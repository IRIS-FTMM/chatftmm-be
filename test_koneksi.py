import requests
import os

# Menghapus setting proxy jika ada, untuk memastikan koneksi langsung
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

print("Mencoba menghubungkan ke https://api.openrouter.ai...")

try:
    # Kita coba akses endpoint /models yang publik
    response = requests.get("https://api.openrouter.ai/api/v1/models", timeout=20)

    print("\n✅ --- KONEKSI BERHASIL! --- ✅")
    print(f"Status Code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print("\n❌ --- KONEKSI GAGAL --- ❌")
    print(f"Detail Error: {e}")