import os

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
ENV_PATH = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    COOKIE_SECURE: bool = True

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
