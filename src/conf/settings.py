import os
from typing import List
from pydantic import BaseSettings
from google.oauth2 import service_account


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REGION: str = "asia-southeast1"
    SERVICE: str = "hive-db"
    VERSION: str = "v1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    PREFIX: str = f"{SERVICE}/{VERSION}"
    GOOGLE_KEY_FILE: str = ".env/Steemit-e706b5b8cead.json"
    HIVE_KEY: str = "WrrXP6szu06wlLQVfAM3b0FD8i4612zc"
    ALLOWED_HOSTS: List[str] = ["*"]

    class Config:
        env_file = ".env"
