# ChatFTMM Backend API

![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-1cc88e.svg)

Ini adalah layanan backend untuk aplikasi **Chatbot FTMM**, sebuah asisten AI yang dirancang untuk memberikan informasi seputar Fakultas Teknologi Maju dan Multidisiplin (FTMM), Universitas Airlangga. Proyek ini dibangun menggunakan FastAPI dan menerapkan arsitektur RAG (Retrieval-Augmented Generation) untuk memberikan jawaban yang akurat berdasarkan basis data dokumen yang relevan.

---

## 🚀 Fitur Utama

-   **API Endpoint Chat**: Menyediakan endpoint `/api/chat` untuk menerima pertanyaan dari pengguna.
-   **Retrieval System**: Menggunakan algoritma **BM25L** untuk mencari dan mengambil dokumen yang paling relevan dari basis data berdasarkan kueri pengguna.
-   **Generative Summarization**: Menggunakan model bahasa dari **OpenRouter** untuk menganalisis konteks dari dokumen yang ditemukan dan menghasilkan jawaban dalam bahasa alami.
-   **Preprocessing Teks**: Melakukan pembersihan, tokenisasi, stemming, dan ekspansi sinonim pada teks untuk meningkatkan akurasi pencarian.
-   **Manajemen Model**: Secara otomatis memuat model yang sudah ada atau membuat dan menyimpan model baru jika tidak ditemukan.

---

## 🛠️ Teknologi yang Digunakan

-   **Framework**: FastAPI
-   **Bahasa**: Python 3.10+
-   **Pemrosesan Bahasa Alami (NLP)**: NLTK, Sastrawi
-   **Manajemen Data**: Pandas, NumPy
-   **Server**: Uvicorn
-   **Layanan LLM**: OpenRouter API

---

## 📂 Struktur Proyek


.
├── .env.example      # Contoh file untuk variabel lingkungan
├── .gitignore        # File yang diabaikan oleh Git
├── artifacts/        # Folder untuk menyimpan model yang sudah dibuat (misal: bm25l_model.pkl)
├── data/             # Folder untuk menyimpan dataset mentah (misal: Dataset.xlsx)
├── main.py           # Titik masuk utama aplikasi FastAPI
├── chatbot.py        # Logika inti alur chatbot (retrieval -> summarization)
├── retrieval.py      # Fungsi-fungsi untuk preprocessing dan pencarian dokumen
├── summarization.py  # Kelas untuk berinteraksi dengan API OpenRouter
├── model_service.py  # Layanan untuk memuat atau membuat model retrieval
├── config.py         # Konfigurasi aplikasi dan variabel lingkungan
├── schemas.py        # Skema data Pydantic untuk validasi request/response
└── requirements.txt  # Daftar pustaka Python yang dibutuhkan


---

## ⚙️ Instalasi dan Pengaturan Lokal

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di mesin lokal Anda.

### 1. Prasyarat

-   Python 3.10 atau lebih baru
-   Git

### 2. Kloning Repositori

```bash
git clone [https://github.com/arknsa/chatftmm-be.git](https://github.com/arknsa/chatftmm-be.git)
cd chatftmm-be

3. Buat dan Aktifkan Virtual Environment
Windows:

python -m venv .venv
.\.venv\Scripts\activate

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

4. Instal Dependensi
Pastikan virtual environment Anda aktif, lalu instal semua pustaka yang dibutuhkan.

pip install -r requirements.txt

5. Unduh Data NLTK
Jalankan skrip berikut untuk mengunduh data stopwords dan punkt dari NLTK.

python download_nltk.py

6. Konfigurasi Variabel Lingkungan
Buat file baru bernama .env di direktori root proyek dan isi dengan format berikut:

# .env

# Ganti dengan API Key Anda dari OpenRouter
OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Ganti dengan URL frontend Anda untuk header referer
HTTP_REFERER="http://localhost:5173"

7. Jalankan Server
Gunakan Uvicorn untuk menjalankan server FastAPI. Flag --reload akan membuat server otomatis restart setiap kali ada perubahan pada kode.

uvicorn main:app --reload

Server sekarang akan berjalan di http://127.0.0.1:8000.

🔌 Endpoint API
POST /api/chat
Endpoint utama untuk berinteraksi dengan chatbot.

Request Body:

{
  "query": "Ada program studi apa saja di FTMM?"
}

Response Sukses (200 OK):

{
  "response": "Di Fakultas Teknologi Maju dan Multidisiplin (FTMM) terdapat beberapa program studi, antara lain Teknologi Sains Data, Teknik Industri, Rekayasa Nanoteknologi, Teknik Robotika dan Kecerdasan Buatan, serta Teknik Elektro."
}

Anda dapat mengakses dokumentasi API interaktif yang dibuat secara otomatis oleh FastAPI di `http://127.0.0.