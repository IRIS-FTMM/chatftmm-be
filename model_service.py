# file: model_service.py (PERBAIKAN INISIALISASI KLIEN)

import os
import pickle
import pandas as pd
from dotenv import load_dotenv
from retrieval import BM25L, preprocess_text
from openai import OpenAI # <-- Tambahkan impor OpenAI
from config import settings # <-- Impor settings untuk API Key

# Memuat .env
load_dotenv()

# --- Variabel Global ---
DF_DATASET = None
DF_KONTEKS = None
BM25L_MODEL = None
openai_client: OpenAI | None = None # <-- Tambahkan variabel untuk klien OpenAI

# --- Path ---
DATASET_PATH = os.path.join("data", "Dataset_Optimized_FTMM_UNAIR.xlsx")
MODEL_CACHE_PATH = os.path.join("artifacts", "bm25l_model.pkl")
DATAFRAME_CACHE_PATH = os.path.join("artifacts", "dataframe_bm25l.pkl")

# --- FUNGSI BARU UNTUK INISIALISASI OPENAI ---
def init_openai_client():
    """Menginisialisasi klien OpenAI sekali saat startup."""
    global openai_client
    try:
        openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        print("✅ Klien OpenAI berhasil diinisialisasi.")
    except Exception as e:
        print(f"❌ GAGAL inisialisasi klien OpenAI: {e}")
# --------------------------------------------

def load_full_dataset():
    """Memuat dataset lengkap dari file Excel."""
    global DF_DATASET
    if DF_DATASET is None:
        print("Memuat dataset lengkap dari Excel...")
        DF_DATASET = pd.read_excel(DATASET_PATH)
        print("Dataset lengkap berhasil dimuat.")
    return DF_DATASET

def load_model_cache():
    # ... (fungsi ini tidak berubah)
    try:
        with open(MODEL_CACHE_PATH, 'rb') as f:
            bm25l = pickle.load(f)
        with open(DATAFRAME_CACHE_PATH, 'rb') as f:
            df_konteks = pickle.load(f)
        print("Model dan DataFrame berhasil dimuat dari cache.")
        return df_konteks, bm25l
    except FileNotFoundError:
        print("Cache tidak ditemukan.")
        return None, None

def save_model_cache(bm25l, df_konteks):
    # ... (fungsi ini tidak berubah)
    os.makedirs("artifacts", exist_ok=True)
    with open(MODEL_CACHE_PATH, 'wb') as f:
        pickle.dump(bm25l, f)
    with open(DATAFRAME_CACHE_PATH, 'wb') as f:
        pickle.dump(df_konteks, f)
    print("Model dan DataFrame berhasil disimpan ke cache.")

def create_bm25l_retrieval_system(data_path):
    # ... (fungsi ini tidak berubah)
    df = pd.read_excel(data_path)
    df['processed_text'] = df['konteks_pencarian'].apply(preprocess_text)
    bm25l = BM25L(df['processed_text'].tolist())
    return df, bm25l