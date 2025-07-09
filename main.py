# main.py
from fastapi import FastAPI
from chat_router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Chatbot FTMM API",
    description="API untuk chatbot informasi Fakultas Teknologi Maju dan Multidisiplin",
    version="1.0.0"
)

# --- PERBAIKAN DI SINI ---
# Tambahkan URL frontend Anda yang sudah di-deploy ke dalam daftar origins.
# Ini akan mengizinkan frontend Anda untuk berkomunikasi dengan backend.
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://chatftmm-fe-production.up.railway.app" # URL Frontend di Railway
]
# --- AKHIR PERBAIKAN ---

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
    print("🚀 Aplikasi FastAPI (Pure API) memulai...")
    print("✅ Server siap menerima permintaan pada endpoint /api/...")