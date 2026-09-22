from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = "todo"


class Settings(BaseSettings):
    # todo

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()  # pyright: ignore[reportCallIssue]
