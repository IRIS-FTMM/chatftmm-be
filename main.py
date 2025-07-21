# file: main.py

from fastapi import FastAPI
from chat_router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
# --- BAGIAN YANG DIUBAH ---
# Impor modulnya, bukan fungsinya secara spesifik
import model_service 
# -------------------------

app = FastAPI(
    title="Chatbot FTMM API",
    description="API untuk chatbot informasi Fakultas Teknologi Maju dan Multidisiplin",
    version="1.0.0"
)

# URL frontend yang diizinkan untuk berkomunikasi dengan backend
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://chatftmm-fe-production.up.railway.app"  # URL Frontend di Railway
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# API Routers
app.include_router(chat_router, prefix="/api", tags=["Chat"])

@app.on_event("startup")
async def startup_event():
    print("🚀 Aplikasi FastAPI memulai...")

    # --- BAGIAN YANG DIUBAH SECARA TOTAL ---
    # 1. Muat dataset lengkap terlebih dahulu
    model_service.load_full_dataset()

    # 2. Coba muat model dari cache
    df_konteks, bm25l = model_service.load_model_cache()

    # 3. Jika cache tidak ada, buat model baru
    if df_konteks is None or bm25l is None:
        print("Cache tidak ada, membangun sistem retrieval baru...")
        df_konteks, bm25l = model_service.create_bm25l_retrieval_system(model_service.DATASET_PATH)
        model_service.save_model_cache(bm25l, df_konteks)
    
    # 4. Simpan model yang sudah siap ke variabel global di model_service
    # INI ADALAH KUNCI UTAMANYA!
    model_service.DF_KONTEKS = df_konteks
    model_service.BM25L_MODEL = bm25l

    print("✅ Server siap menerima permintaan.")
    # ----------------------------------------