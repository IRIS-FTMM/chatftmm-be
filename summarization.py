# file: summarization.py (FINAL DENGAN PENANGANAN AMBIGUITAS & SINONIM)

import requests
import json
import time
from config import settings

class Summarizer:
    def summarize(self, query: str, contexts: list[str]) -> str:
        """
        Mengirim konteks ke API LLM dan mengembalikan jawaban yang sudah diringkas
        dengan penanganan konteks spesifik FTMM.
        """
        combined_context = "\n\n---\n\n".join(contexts)

        # Prompt yang disempurnakan dengan instruksi penanganan ambiguitas
        prompt = f"""
        Anda adalah asisten AI ahli dari Fakultas Teknologi Maju dan Multidisiplin (FTMM) Universitas Airlangga.
        Anda harus menjawab dengan SANGAT AKURAT berdasarkan konteks yang diberikan dan mengikuti semua peraturan.

        **PERATURAN UTAMA & KONTEKS SPESIFIK FTMM:**
        1.  **Akurasi Tinggi**: Jawaban HARUS diambil murni dari teks dalam `KONTEKS`. Jangan menggunakan pengetahuan eksternal.
        2.  **Presisi Nama & Gelar**: Saat menyebutkan nama orang, Anda WAJIB menyalin NAMA LENGKAP beserta SEMUA GELAR AKADEMIK persis seperti yang tertulis. JANGAN menyingkat atau mengubah format.
        3.  **PENANGANAN SINGKATAN (SANGAT PENTING!):**
            * Singkatan **"TI"** dalam konteks FTMM selalu merujuk pada **"Teknik Industri"**, BUKAN "Teknologi Informasi". Selalu gunakan nama lengkap "Teknik Industri" saat menjawab.
            * Singkatan **"TSD"** merujuk pada **"Teknologi Sains Data"**.
            * Singkatan **"TRKB"** merujuk pada **"Teknik Robotika dan Kecerdasan Buatan"**.
            * Singkatan **"TE"** merujuk pada **"Teknik Elektro"**.
            * Singkatan **"RN"** merujuk pada **"Rekayasa Nanoteknologi"**.
        4.  **PENANGANAN SINONIM:**
            * Istilah **"Organisasi"** dan **"ORMAWA"** (Organisasi Mahasiswa) merujuk pada hal yang sama. Jika ditanya salah satunya, berikan daftar ORMAWA lengkap yang ada (BEM, BLM, Himpunan Mahasiswa).
        5.  **Gunakan Markdown**: Format jawaban Anda menggunakan Markdown untuk kejelasan.
            * Gunakan `**teks tebal**` untuk nama orang, jabatan, dan nama program studi lengkap.
            * Gunakan `*teks miring*` untuk nama acara, kompetisi, atau inovasi.
        6.  **Kejujuran**: Jika informasi tidak ada di dalam `KONTEKS`, jawab dengan jujur bahwa Anda tidak dapat menemukannya.

        **KONTEKS YANG RELEVAN:**
        ---
        {combined_context}
        ---

        **PERTANYAAN PENGGUNA:**
        "{query}"

        **JAWABAN AKURAT, TERFORMAT, DAN SADAR-KONTEKS:**
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Percobaan ke-{attempt + 1} untuk menghubungi API OpenAI...")
                # Di sini Anda akan menggunakan klien OpenAI yang sudah diinisialisasi
                # (Asumsi Anda sudah beralih dari OpenRouter ke OpenAI seperti percakapan sebelumnya)
                # Jika masih menggunakan OpenRouter, sesuaikan kembali.
                
                # Contoh menggunakan OpenAI client (pastikan sudah diinisialisasi di tempat lain)
                from model_service import client as openai_client # Contoh impor
                if not openai_client:
                    return "Klien OpenAI tidak terinisialisasi."

                response = openai_client.chat.completions.create(
                    model="gpt-4.1-mini", # Atau model lain yang Anda pilih
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=0.1
                )
                
                content = response.choices[0].message.content
                if content:
                    print("Respons AI berhasil diterima.")
                    return content.strip()
                
            except Exception as e:
                print(f"Error pada percobaan ke-{attempt+1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    return "Maaf, terjadi kesalahan setelah beberapa kali percobaan."

        return "Maaf, saya tidak dapat memproses permintaan Anda saat ini."