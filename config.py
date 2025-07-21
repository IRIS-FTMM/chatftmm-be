# file: config.py (PERBAIKAN FINAL UNTUK DEPLOYMENT)

from pydantic_settings import BaseSettings

# Dengan menghapus 'SettingsConfigDict', Pydantic akan secara otomatis
# membaca variabel dari lingkungan (seperti di Railway)
# dan juga akan tetap membaca dari file .env saat Anda menjalankan di lokal.
# Ini adalah cara yang paling fleksibel dan tangguh.

class Settings(BaseSettings):
    # Variabel yang dibutuhkan dari environment
    OPENROUTER_API_KEY: str
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    HTTP_REFERER: str

    # Variabel dengan nilai default (tidak perlu ada di environment)
    ARTIFACTS_DIR: str = "artifacts"
    DATA_DIR: str = "data"

settings = Settings()