from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token
from src.db.redis import token_in_blocklist

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
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
                if await token_in_blocklist(token_data['jti']):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has been revoked.")
                self.verify_token_data(token_data)
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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please use access token instead of refresh token.")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please use refresh token instead of access token.")