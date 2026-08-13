# Engine + SessionLocal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

DATABASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    app_name: str
    app_env: str

    database_url: str

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool = False

    model_config = SettingsConfigDict(
        env_file= DATABASE_DIR /".env",
        case_sensitive=False,
    )


settings = Settings()