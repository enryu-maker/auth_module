from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    # Basic Project Settings
    PROJECT_NAME: str = "Auth Module"
    PROJECT_DESCRIPTION: str = "A production-ready Auth Module application."
    PROJECT_VERSION: str = "1.0.0"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database settings
    # Example for SQLite; replace with your actual DB URL
    DATABASE_URL: str = "postgresql://postgres:Akif1432@localhost/auth"

    # Security settings
    SECRET_KEY: str = "e15a39ceb9a4d577df8cc72c2e4462c980fb1459f16af8bbbe92d900e79a0934"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    # HTTPS enforcement (optional)
    ENFORCE_HTTPS: bool = False

    # Allowed Hosts
    ALLOWED_HOSTS: List[str] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, list):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"  # Load environment variables from a .env file


# Create an instance of the Settings class
settings = Settings()
