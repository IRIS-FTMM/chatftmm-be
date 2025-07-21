# file: model_service.py

import os
import pickle
import pandas as pd
# Hapus joblib jika tidak digunakan, dan numpy jika tidak digunakan di sini
from dotenv import load_dotenv
from retrieval import BM25L, preprocess_text # Pastikan import ini benar

# Memuat .env
load_dotenv()

# --- BAGIAN YANG DIUBAH ---
# Variabel Global untuk menyimpan model dan data yang sudah dimuat
# Ini akan diisi saat aplikasi FastAPI startup.
DF_DATASET = None # DataFrame asli, lengkap
DF_KONTEKS = None # DataFrame yang diproses untuk retrieval
BM25L_MODEL = None # Model BM25L yang sudah dilatih
# -------------------------

# Path untuk dataset dan cache embedding
DATASET_PATH = os.path.join("data", "Dataset_Optimized.xlsx")
MODEL_CACHE_PATH = os.path.join("artifacts", "bm25l_model.pkl")
DATAFRAME_CACHE_PATH = os.path.join("artifacts", "dataframe_bm25l.pkl")


def load_full_dataset():
    """Memuat dataset lengkap dari file Excel."""
    global DF_DATASET
    if DF_DATASET is None:
        print("Memuat dataset lengkap dari Excel...")
        DF_DATASET = pd.read_excel(DATASET_PATH)
        print("Dataset lengkap berhasil dimuat.")
    return DF_DATASET


# Cek apakah model BM25L dan DataFrame sudah ada di cache
def load_model_cache():
    # ... (fungsi ini tetap sama)
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


# Simpan BM25L dan DataFrame ke dalam cache
def save_model_cache(bm25l, df_konteks):
    # ... (fungsi ini tetap sama)
    os.makedirs("artifacts", exist_ok=True)
    with open(MODEL_CACHE_PATH, 'wb') as f:
        pickle.dump(bm25l, f)
    with open(DATAFRAME_CACHE_PATH, 'wb') as f:
        pickle.dump(df_konteks, f)
    print("Model dan DataFrame berhasil disimpan ke cache.")


# Fungsi untuk membuat model BM25L dan DataFrame
def create_bm25l_retrieval_system(data_path):
    # ... (fungsi ini tetap sama)
    df = pd.read_excel(data_path)
    # Gunakan 'konteks_pencarian' seperti yang Anda lakukan
    df['processed_text'] = df['konteks_pencarian'].apply(preprocess_text)
    bm25l = BM25L(df['processed_text'].tolist())
    # Kembalikan DataFrame yang sudah diproses, bukan yang mentah
    return df, bm25l

# HAPUS FUNGSI INI UNTUK MENGHINDARI KEBINGUNGAN
# Fungsi search_documents(query, top_k=5) tidak lagi diperlukan di sini
# karena logika pencarian sudah ada di retrieval.py dan dipanggil dari chatbot.py