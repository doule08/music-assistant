from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    dlna_url: str
    navidrome_url: str
    wiim_url: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()  # pyright: ignore[reportCallIssue]
