# file: backend/setup.py
import nltk

print("--- Memulai setup pra-deployment ---")
print("Mengunduh paket data NLTK yang dibutuhkan...")
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    print("✅ Paket data NLTK ('punkt', 'stopwords') berhasil diunduh.")
except Exception as e:
    print(f"❌ Gagal mengunduh paket NLTK: {e}")
print("--- Setup pra-deployment selesai ---")