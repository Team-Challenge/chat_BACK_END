import os
from pathlib import Path
from typing import Optional, Any

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = f"{Path(__file__).parent.parent.parent.absolute()}/.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH)

    SECRET: str
    PAGINATION_SIZE: int

    ROOT_PATH: Optional[Any] = Path(__file__).resolve().parent.parent.parent
    DB_PATH: Optional[Any] = os.path.join(ROOT_PATH, "chat.db")
    SQLITE_URL: Optional[Any] = "sqlite:///" + DB_PATH


settings = Settings()
