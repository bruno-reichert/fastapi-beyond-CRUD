from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from .schemas import UserCreateModel, UserResponseModel, UserLoginModel, UserBooksModel, EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, decode_token, verify_password, create_url_safe_token, decode_url_safe_token, generate_password_hash
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker # type: ignore
from src.db.redis import add_jti_to_blocklist
from src.db.main import get_session
from src.errors import *
from src.mail import mail, create_message
from src.mail_test import send_mailtrap_api
from src.config import Config
from src.celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])


@auth_router.post('/send_mail')
async def send_mail(emails:EmailModel, bg_tasks: BackgroundTasks):
    html = "<h1>Welcome to the app!</h1>"
    subject = "Welcome to the app!"
    try: 
        message = create_message(
        emails, # type: ignore
        "Welcome",
        html
        )
        await mail.send_message(message)
        bg_tasks.add_task(mail.send_message, message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    # await mail.send_message(message)
    return {"message": "Email sent successfully!"}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, bg_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """
    bg_tasks.add_task(
        send_mailtrap_api,
        recipients=[email],
        subject="Verify your email",
        html_content=html_message
    )


    # await mail.send_message(message)

    return {
        "message": "Account created successfully, check email to verify it!",
        "user": new_user
    }

@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    if token_data is not None:
        user_email = token_data.get('email')
        if user_email:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise UserNotFound()
            await user_service.update_user(user, {'is_verified': True}, session)
            return JSONResponse(
                content={"message": "User verified successfully!"}, 
                status_code=status.HTTP_200_OK
            )
        return JSONResponse(content={"message": "Error occured during verification"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return {'oops': 'wtfffff'}

@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(user_data = {"email": user.email, "user_uid": str(user.uid), "role": user.role})
            refresh_token = create_access_token(user_data = {"email": user.email, "user_uid": str(user.uid)}, expires = timedelta(days=2), refresh=True)
            return JSONResponse(content = {
                "message": "Login successful",
                "access_token": access_token, 
                "refresh_token": refresh_token,
                "user": {
                    "email": user.email,
                    "uid": str(user.uid),
                    }
                })
    raise InvalidCredentials()

@auth_router.post('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer()), session: AsyncSession = Depends(get_session)):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data = token_details['user'])
        return JSONResponse(content = {
            "message": "Token refreshed successfully",
            "access_token": new_access_token
        })
    raise InvalidToken()

@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _: bool = Depends(role_checker)):
    if user:
       return user
    raise UserNotFound()

@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(content = {"message": "Logout successful, token revoked"})

@auth_router.post('/password-reset-request')
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email
    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
    html_message = f"""
    <h1>Reset your password</h1>
    <p>Please click this <a href="{link}">link</a> to reset your password</p>
    """
    message = create_message(
        recipients=[email],
        subject="Reset your password",
        body=html_message
    )

    try:
        await mail.send_message(message)
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email"
        )

    return JSONResponse(
        content={
            "message": "Check your email for instructions on how to reset your password!"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post('/password-reset-confirm/{token}')
async def reset_account_password(token: str, passwords: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):
    new_password = passwords.new_password
    confirm_new_password = passwords.confirm_new_password
    if new_password != confirm_new_password:
        raise HTTPException(detail="Passwords do not match", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    token_data = decode_url_safe_token(token)
    if token_data is not None:
        user_email = token_data.get('email')
        if user_email:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise UserNotFound()
            password_hash = generate_password_hash(new_password)
            await user_service.update_user(user, {'password_hash': password_hash}, session)
            return JSONResponse(
                content={"message": "Password reset successfully!"}, 
                status_code=status.HTTP_200_OK
            )
        return JSONResponse(content={"message": "Error occured during password_reset"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return {'oops': 'wtfffff'}