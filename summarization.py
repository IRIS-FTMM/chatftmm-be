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
        # PROMPT ULTIMATE FINAL v2 - Dengan Aturan Anti-Kesalahan TI
        # ===================================================================
        prompt = f"""
Anda adalah asisten AI dari Fakultas Teknologi Maju dan Multidisiplin (FTMM) Universitas Airlangga.
Anda harus menjawab dengan **SANGAT AKURAT, ringkas, dan profesional** berdasarkan `KONTEKS` yang diberikan. Ikuti semua peraturan di bawah ini.

**PERATURAN WAJIB (HARUS DIIKUTI):**

1.  **ATURAN PALING PENTING DAN TIDAK BOLEH DILANGGAR:**
    * Singkatan **"TI"** dalam konteks FTMM **SELALU DAN HANYA** berarti **"Teknik Industri"**.
    * **DILARANG KERAS** menjawab atau berasumsi bahwa "TI" adalah "Teknologi Informasi".
    * Jika Anda melanggar aturan ini, jawaban Anda dianggap gagal total. Ulangi: **TI ADALAH TEKNIK INDUSTRI.**

2.  **SUMBER TUNGGAL**: Jawaban HARUS 100% berdasarkan informasi dari `KONTEKS`. DILARANG KERAS menggunakan pengetahuan eksternal.

3.  **ATURAN SPESIFIK LAINNYA**:
    * **ATURAN DEKAN**: Jika ditanya tentang **"Dekan"**, bedakan dengan jelas antara **Plt. Dekan saat ini (Prof. Ni'matuzahroh)** dan **Dekan terdahulu (Prof. Dwi Setyawan)**. Jangan gabungkan informasi mereka.
    * Jika ditanya nama pimpinan (Kaprodi, Presbem, Ketua BSO, dll), sebutkan nama lengkapnya jika tersedia di konteks.
    * Jika ditanya daftar (dosen, prodi, BSO), gunakan format daftar atau sebutkan semuanya.

4.  **FORMAT JAWABAN**:
    * Gunakan Markdown (`**teks tebal**`) untuk membuat jawaban mudah dibaca.
    * **Langsung ke Inti Jawaban**: Hindari kalimat pembuka yang tidak perlu.

5.  **KEJUJURAN MUTLAK**: Jika informasi yang diminta pengguna TIDAK ADA di dalam `KONTEKS`, jawab HANYA dengan kalimat: **"Maaf, saya tidak dapat menemukan informasi spesifik mengenai hal tersebut."**

---
**KONTEKS YANG RELEVAN:**
{combined_context}
---

**PERTANYAAN PENGGUNA:**
"{query}"

**JAWABAN AKURAT, TERFORMAT, DAN PATUH PADA SEMUA ATURAN DI ATAS:**
"""
        # ===================================================================

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Percobaan ke-{attempt + 1} untuk menghubungi OpenAI API...")
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.0
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