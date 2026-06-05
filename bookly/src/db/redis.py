import redis.asyncio as redis
from src.config import Config

TOKEN_EXPIRY = 3600

token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True,
    protocol=2
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=TOKEN_EXPIRY
    )

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) == 1