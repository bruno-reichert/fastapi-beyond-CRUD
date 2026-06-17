from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    DATABASE_URL : str = ""
    JWT_SECRET_KEY : str = ""
    JWT_ALGORITHM : str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    MAILTRAP_API_TOKEN: str
    MAILTRAP_INBOX_ID: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings() # type: ignore

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL