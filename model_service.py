# model_service.py
import os
import dill
import pandas as pd
from retrieval import create_bm25l_retrieval_system
from config import settings

def load_models():
    model_path = os.path.join(settings.ARTIFACTS_DIR, 'bm25l_model.pkl')
    df_path = os.path.join(settings.ARTIFACTS_DIR, 'dataframe_bm25l.pkl')

    if not os.path.exists(model_path) or not os.path.exists(df_path):
        print("Model tidak ditemukan. Membuat sistem baru...")
        return create_and_save_new_system()
    try:
        with open(model_path, 'rb') as f_model, open(df_path, 'rb') as f_df:
            bm25l = dill.load(f_model)
            df_konteks = dill.load(f_df)
        print("✅ Model berhasil dimuat dari artifacts.")
        return df_konteks, bm25l
    except Exception as e:
        print(f"Gagal memuat model: {e}. Membuat sistem baru...")
        return create_and_save_new_system()

def create_and_save_new_system():
    konteks_path = os.path.join(settings.DATA_DIR, 'Data Konteks txt.xlsx')
    df_konteks, bm25l = create_bm25l_retrieval_system(konteks_path)
    if df_konteks is not None and bm25l is not None:
        os.makedirs(settings.ARTIFACTS_DIR, exist_ok=True)
        model_path = os.path.join(settings.ARTIFACTS_DIR, 'bm25l_model.pkl')
        df_path = os.path.join(settings.ARTIFACTS_DIR, 'dataframe_bm25l.pkl')
        with open(model_path, 'wb') as f_model, open(df_path, 'wb') as f_df:
            dill.dump(bm25l, f_model)
            dill.dump(df_konteks, f_df)
        print("✅ Sistem retrieval baru berhasil dibuat dan disimpan.")
    return df_konteks, bm25l

print("🚀 Memuat model dan data saat aplikasi dimulai...")
DF_KONTEKS, BM25L_MODEL = load_models()
DATASET_PATH = os.path.join(settings.DATA_DIR, 'Dataset.xlsx')
DF_DATASET = pd.read_excel(DATASET_PATH)
print("✨ Model dan data siap digunakan.")