# Nama file: data_optimizer.py
# Skrip ini digunakan untuk membuat dataset yang dioptimalkan untuk pencarian.
# Jalankan skrip ini HANYA SEKALI atau setiap kali Anda memiliki data scraping baru.

import pandas as pd
import os

# --- KONFIGURASI ---
# Pastikan nama file ini sesuai dengan file hasil scraping Anda
SOURCE_FILE = "Data_Hasil_Scraping_Lengkap.xlsx"
# Nama file output yang akan digunakan oleh chatbot
OUTPUT_FILE = "Dataset_Optimized.xlsx"
# Lokasi folder data
DATA_DIR = "data"

def create_search_context(row):
    """Menggabungkan judul dan 50 kata pertama dari isi file."""
    try:
        title = str(row['Judul'])
        content = str(row['Isi File'])
        
        # Ambil 50 kata pertama dari konten
        first_50_words = " ".join(content.split()[:50])
        
        # Gabungkan dengan pengulangan judul untuk memberinya bobot lebih
        # Ini adalah trik umum untuk meningkatkan relevansi pencarian
        search_context = f"{title}. {title}. {title}. {first_50_words}"
        return search_context
    except Exception:
        return str(row['Judul']) # Fallback jika ada error

def main():
    """Fungsi utama untuk menjalankan proses optimasi."""
    print("🚀 Memulai proses optimasi dataset...")
    
    source_path = os.path.join(DATA_DIR, SOURCE_FILE)
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)

    if not os.path.exists(source_path):
        print(f"[X] ERROR: File sumber '{source_path}' tidak ditemukan.")
        print("Pastikan file hasil scraping Anda ada di dalam folder 'data'.")
        return

    print(f"[*] Membaca data dari: {source_path}")
    df = pd.read_excel(source_path)

    print("[*] Membuat kolom 'konteks_pencarian' yang dioptimalkan...")
    df['konteks_pencarian'] = df.apply(create_search_context, axis=1)

    # Memilih kolom yang akan disimpan ke file final
    # Kita tidak perlu menyimpan 'Path File' atau 'Isi File' yang diproses ulang
    # karena sudah ada di file aslinya.
    final_df = df[['Index', 'Judul', 'Sumber', 'konteks_pencarian', 'Isi File']]

    print(f"[*] Menyimpan dataset yang dioptimalkan ke: {output_path}")
    final_df.to_excel(output_path, index=False)

    print("\n" + "="*50)
    print("✅ Proses optimasi selesai!")
    print(f"File '{OUTPUT_FILE}' telah dibuat di dalam folder '{DATA_DIR}'.")
    print("Anda sekarang bisa me-restart server chatbot Anda.")
    print("="*50)

if __name__ == "__main__":
    main()
