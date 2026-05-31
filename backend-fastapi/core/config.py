from pydantic_settings import BaseSettings
from datetime import timedelta


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool = False
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    class Config:
        env_file = ".env"


settings = Settings()
