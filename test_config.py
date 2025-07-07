# file: backend/test_config.py

import os

print("Mencoba memuat konfigurasi secara langsung...")
print(f"Direktori kerja saat ini: {os.getcwd()}")
print("-" * 20)

try:
    # Kita coba import 'settings' dari file config Anda
    from config import settings

    # Jika berhasil, kita cetak isinya untuk membuktikan sudah terbaca
    print("✅ Konfigurasi berhasil dimuat.")
    print(f"API Key Terbaca: ...{settings.OPENROUTER_API_KEY[-4:]}") # Hanya cetak 4 digit terakhir untuk keamanan
    print(f"HTTP Referer Terbaca: {settings.HTTP_REFERER}")

except Exception as e:
    # Jika gagal, kita akan tahu apa error pastinya
    print("❌ GAGAL memuat konfigurasi.")
    print("\n--- ERROR DETAIL ---")
    print(e)
    print("--------------------")