# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    OPENROUTER_API_KEY: str
    HTTP_REFERER: str
    ARTIFACTS_DIR: str = "artifacts"
    DATA_DIR: str = "data"

settings = Settings()