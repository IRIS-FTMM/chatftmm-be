# file: backend/setup.py (VERSI DISEMPURNAKAN)
import nltk

print("--- Memulai setup pra-deployment ---")
print("Mengunduh semua paket data NLTK yang dibutuhkan...")

# Daftar sumber daya yang diperlukan
resources = ['punkt', 'stopwords', 'punkt_tab'] 

try:
    for resource in resources:
        print(f"--> Mengunduh '{resource}'...")
        nltk.download(resource)
    print("✅ Semua paket data NLTK berhasil diunduh.")
except Exception as e:
    print(f"❌ Gagal mengunduh salah satu paket NLTK: {e}")

print("--- Setup pra-deployment selesai ---")