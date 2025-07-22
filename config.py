# file: config.py (PERBAIKAN FINAL UNTUK LOKAL & DEPLOYMENT)

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# --- KUNCI PERBAIKAN ADA DI SINI ---
# Secara manual memuat file .env yang ada di direktori yang sama
# Ini memastikan variabel lingkungan selalu termuat, baik di lokal maupun di server.
# Jika file .env tidak ada (seperti di Railway), fungsi ini tidak akan error.
load_dotenv()
# ------------------------------------

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

# Verifikasi (opsional, tapi bagus untuk debugging)
print("✅ Variabel berhasil dimuat:")
print(f"   OPENAI_API_KEY: {'*' * (len(settings.OPENAI_API_KEY) - 4) + settings.OPENAI_API_KEY[-4:] if settings.OPENAI_API_KEY else 'None'}")
print(f"   PINECONE_API_KEY: {'*' * (len(settings.PINECONE_API_KEY) - 4) + settings.PINECONE_API_KEY[-4:] if settings.PINECONE_API_KEY else 'None'}")