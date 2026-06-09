from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from src.db.models import User
from src.errors import *
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import List

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | dict | None: # type: ignore
        creds = await super().__call__(request)
        if creds:
            tokens = creds.credentials
            token_data = decode_token(tokens)
            if token_data:
                if not self.token_valid(tokens):
                    raise InvalidToken()
                if await token_in_blocklist(token_data['jti']):
                    raise InvalidToken()
                return token_data
        return None
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False
    
    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Subclasses must implement this method!!!")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()
        

async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()), 
    session: AsyncSession = Depends(get_session)
    ):
    if token_details is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing token.")
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(session=session, email=user_email)
    if user:
        return user
    return None

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()