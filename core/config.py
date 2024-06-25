import pathlib

from pydantic import AnyHttpUrl,  EmailStr, field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Union


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_V1_STR: str = "/"
    JWT_SECRET: str = "b597ea124e1a892aa4a3852f08a5d04b84256ee50b413c55f82ac6570edd7658"
    JWT_REFRESH_SECRET: str = "9e3fd20b605825d61e731d14b7e265594d5da1d47cb5af1619e3ca17fab0c123"
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    SQLALCHEMY_DATABASE_URI: Optional[str] = f"sqlite:///./mach.db"
    FIRST_SUPERUSER: EmailStr = "aruljoshua@gmail.com"
    FIRST_SUPERUSER_PW: str = "12345678"

    class Config:
        case_sensitive = True
settings = Settings()