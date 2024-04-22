# Pydantic Import
from pydantic_settings import BaseSettings
from decouple import config
from typing import Optional


class Settings(BaseSettings):
    """Base configuration settings"""

    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str)
    TOKEN_LIFETIME: int = config("TOKEN_LIFETIME", cast=int)
    # # USE_TEST_DB: bool = config("USE_TEST_DB", cast=bool)
    # USE_TEST_DB: Optional[bool] is None

    TITLE: str = "Hospital Management System"
    DESCRIPTION: str = ""


hms_settings = Settings()
