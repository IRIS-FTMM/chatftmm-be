# file: summarization.py (PERBAIKAN CARA MENGGUNAKAN KLIEN)

import time
from openai import RateLimitError, APIConnectionError, APIStatusError
import model_service # <-- Impor seluruh modul

class Summarizer:
    def summarize(self, query: str, contexts: list[str]) -> str:
        # Cek apakah klien sudah siap dari model_service
        client = model_service.openai_client
        if not client:
            return "Maaf, koneksi ke layanan AI tidak siap. Periksa log server."

        combined_context = "\n\n---\n\n".join(contexts)
        
        # Prompt lengkap Anda (tidak ada perubahan di sini)
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
                print(f"Percobaan ke-{attempt + 1} untuk menghubungi OpenAI API...")
                
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400,
                    temperature=0.1
                )
                
                content = response.choices[0].message.content
                if content:
                    print("Respons dari OpenAI API berhasil diterima.")
                    return content.strip()
                else:
                    return "Maaf, AI memberikan respons kosong."

            except RateLimitError as e:
                wait_time = (2 ** attempt) * 5
                print(f"Terkena rate limit. Mencoba lagi dalam {wait_time} detik... Error: {e}")
                time.sleep(wait_time)
            
            except (APIConnectionError, APIStatusError) as e:
                print(f"Error koneksi atau status dari OpenAI API: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return "Maaf, terjadi masalah koneksi saat menghubungi server OpenAI."
            
            except Exception as e:
                print(f"Terjadi error tak terduga: {e}")
                return "Maaf, terjadi kesalahan internal yang tidak terduga."

        return "Maaf, saya tidak dapat memproses permintaan Anda setelah beberapa kali percobaan."