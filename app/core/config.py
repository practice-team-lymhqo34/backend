from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "logiflow"

    # Додай цей рядок
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    SECRET_KEY: str = "temporary_secret_for_dev_only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    COOKIE_SECURE: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
