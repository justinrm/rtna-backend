from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "rTNA Platform"
    APP_VERSION: str = "1.0.2"
    SECRET_KEY: str = "your_secret_key_here"


    # Database settings
    DATABASE_URL: str

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS settings
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()

