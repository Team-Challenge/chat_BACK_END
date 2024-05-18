import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Union, Literal

from pydantic import PostgresDsn, field_validator, EmailStr
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

# from pytz import timezone

ENV_PATH = f"{Path(__file__).parent.parent.parent.absolute()}/.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH)

    SECRET: str
    PAGINATION_SIZE: int

    ROOT_PATH: Optional[Any] = Path(__file__).resolve().parent.parent.parent
    DB_PATH: Optional[Any] = os.path.join(ROOT_PATH, "chat.db")
    SQLITE_URL: Optional[Any] = "sqlite:///" + DB_PATH


settings = Settings()
# TIMEZONE = timezone('Europe/Kyiv')


# def default_time():
#     return datetime.now(tz=TIMEZONE)
