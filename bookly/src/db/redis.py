import redis.asyncio as redis
from src.config import Config

TOKEN_EXPIRY = 3600

token_blocklist = redis.from_url(Config.REDIS_URL)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=TOKEN_EXPIRY
    )

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) == 1

# admin
admin_permissions = [
    "adding users",
    "change roles",
    "crud on users",
    "book submissions",
    "crud on reviews",
    "revoking access"
]

# user
user_permissions = [
    "crud on their own book submissions",
    "crud on their own reviews",
    "crud on their own accounts"
]