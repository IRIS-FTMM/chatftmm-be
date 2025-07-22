# file: config.py (VERSI FINAL)
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Memuat .env secara manual untuk development lokal
load_dotenv()

class Settings(BaseSettings):
    # Variabel yang dibutuhkan dari environment
    OPENROUTER_API_KEY: str
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    HTTP_REFERER: str

    # Variabel dengan nilai default
    ARTIFACTS_DIR: str = "artifacts"
    DATA_DIR: str = "data"

settings = Settings()