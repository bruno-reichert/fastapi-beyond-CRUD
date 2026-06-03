import logging
import bcrypt
from datetime import datetime, timedelta, timezone
from src.config import Config
import jwt
import uuid

ACCESS_TOKEN_EXPIRE_MINUTES = 60

def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash.encode())

def create_access_token(user_data: dict, expires: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), refresh: bool = False) -> str:
    payload = {}

    payload['user'] = user_data
    payload['exp'] = int((datetime.now(timezone.utc) + expires).timestamp())
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET_KEY,
        algorithm = Config.JWT_ALGORITHM,
    )
    return token

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            jwt = token,
            key = Config.JWT_SECRET_KEY,
            algorithms = [Config.JWT_ALGORITHM],
        )
        return payload
    except jwt.PyJWTError as e:
        logging.exception(f"Error decoding token: {e}")
        return None