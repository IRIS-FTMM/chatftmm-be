# file: main.py (PERBAIKAN CORS)

from fastapi import FastAPI
from chat_router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import model_service

app = FastAPI(
    title="Chatbot FTMM API",
    description="API untuk chatbot informasi Fakultas Teknologi Maju dan Multidisiplin",
    version="1.0.0"
)

# --- PERUBAHAN PENTING ADA DI SINI ---
# Tambahkan URL frontend Anda yang sudah di-deploy ke dalam daftar origins
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://chatftmm-fe-production-9d80.up.railway.app", # <-- URL BARU DITAMBAHKAN
]
# ------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Izinkan semua metode (GET, POST, dll)
    allow_headers=["*"], # Izinkan semua header
)

# API Routers
app.include_router(chat_router, prefix="/api", tags=["Chat"])

@app.on_event("startup")
async def startup_event():
    print("🚀 Aplikasi FastAPI memulai...")

    # Inisialisasi Klien OpenAI (PENTING untuk perbaikan kedua)
    model_service.init_openai_client()

    # Memuat dataset lengkap terlebih dahulu
    model_service.load_full_dataset()

    # Coba muat model cache BM25L
    df_konteks, bm25l = model_service.load_model_cache()

    if df_konteks is None or bm25l is None:
        print("Cache tidak ada, membangun sistem retrieval baru...")
        df_konteks, bm25l = model_service.create_bm25l_retrieval_system(model_service.DATASET_PATH)
        model_service.save_model_cache(bm25l, df_konteks)
    
    # Simpan model yang sudah siap ke variabel global
    model_service.DF_KONTEKS = df_konteks
    model_service.BM25L_MODEL = bm25l

    print("✅ Server siap menerima permintaan.")