# file: backend/download_nltk.py

import nltk

print("Mencoba mengunduh data NLTK yang dibutuhkan...")

resources_to_download = ['punkt', 'stopwords', 'punkt_tab']

for resource in resources_to_download:
    try:
        print(f"Mengunduh '{resource}'...")
        nltk.download(resource)
        print(f"'{resource}' berhasil diunduh.")
    except Exception as e:
        print(f"Gagal mengunduh '{resource}': {e}")

print("\nProses download selesai.")