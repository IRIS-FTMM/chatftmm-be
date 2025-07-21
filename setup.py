# file: backend/setup.py

import nltk

print("Mengunduh paket data NLTK...")
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    print("Paket data NLTK berhasil diunduh.")
except Exception as e:
    print(f"Gagal mengunduh paket NLTK: {e}")