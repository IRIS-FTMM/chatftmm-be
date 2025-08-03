import time
from openai import RateLimitError, APIConnectionError, APIStatusError
import model_service # Impor seluruh modul

class Summarizer:
    def summarize(self, query: str, contexts: list[str]) -> str:
        # Cek apakah klien sudah siap dari model_service
        client = model_service.openai_client
        if not client:
            return "Maaf, koneksi ke layanan AI tidak siap. Periksa log server."

        combined_context = "\n\n---\n\n".join(contexts)
        
        # ===================================================================
        # PROMPT FINAL - Dirancang untuk Bekerja dengan Data Pinecone Baru
        # ===================================================================
        prompt = f"""
Anda adalah asisten AI dari Fakultas Teknologi Maju dan Multidisiplin (FTMM) Universitas Airlangga.
Anda harus menjawab dengan **SANGAT AKURAT, ringkas, dan profesional** berdasarkan `KONTEKS` yang diberikan. Ikuti semua peraturan di bawah ini.

**PERATURAN WAJIB:**
1.  **SUMBER TUNGGAL**: Jawaban HARUS 100% berdasarkan informasi dari `KONTEKS`. DILARANG KERAS menggunakan pengetahuan eksternal atau membuat asumsi.
2.  **MENJAWAB PERTANYAAN SPESIFIK**:
    * **PERHATIAN KHUSUS UNTUK DEKAN**: Jika ditanya tentang **"Dekan"**, jawaban Anda HARUS membedakan dengan jelas antara **Plt. Dekan saat ini (Prof. Ni'matuzahroh)** dan **Dekan terdahulu (Prof. Dwi Setyawan)**. Jangan gabungkan informasi mereka. Sebutkan jabatan baru Prof. Dwi Setyawan jika ada di konteks.
    * Jika ditanya tentang singkatan prodi (misal: "apa itu RN"), berikan nama lengkapnya: **Rekayasa Nanoteknologi**.
    * Jika ditanya daftar prodi, sebutkan kelima prodi yang ada di konteks.
3.  **FORMAT JAWABAN**:
    * Gunakan Markdown (`**teks tebal**`) untuk membuat jawaban mudah dibaca.
    * **Langsung ke Inti Jawaban**: Hindari kalimat pembuka yang tidak perlu.
4.  **KEJUJURAN MUTLAK**: Jika informasi yang diminta pengguna TIDAK ADA di dalam `KONTEKS`, jawab HANYA dengan kalimat: **"Maaf, saya tidak dapat menemukan informasi spesifik mengenai hal tersebut."**

---
**KONTEKS YANG RELEVAN:**
{combined_context}
---

**PERTANYAAN PENGGUNA:**
"{query}"

**JAWABAN AKURAT, TERFORMAT, DAN SADAR-KONTEKS:**
"""
        # ===================================================================

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Percobaan ke-{attempt + 1} untuk menghubungi OpenAI API...")
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Menggunakan gpt-4o-mini lebih baru dan efisien
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500, # Dinaikkan sedikit untuk mengakomodasi jawaban tabel
                    temperature=0.0 # Dibuat 0.0 untuk jawaban yang paling deterministik dan akurat
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