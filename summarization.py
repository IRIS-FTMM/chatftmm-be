# app/core/summarization.py

import requests
import json
from config import settings

class Summarizer:
    def summarize(self, query: str, contexts: list[str]) -> str:
        """
        Buat rangkuman berdasarkan query dan konteks dokumen menggunakan model di OpenRouter
        dengan panggilan API langsung menggunakan pustaka 'requests'.
        """
        
        # Menggabungkan semua konteks menjadi satu blok teks yang terstruktur
        combined_context = "\n\n---\n\n".join(contexts)

        # --- CHAIN-OF-THOUGHT (CoT) PROMPT ---
        # Prompt ini tetap sama, menginstruksikan model untuk berpikir secara bertahap.
        prompt = f"""
        Anda adalah asisten AI dari Fakultas Teknologi Maju dan Multidisiplin (FTMM) Universitas Airlangga.
        Tugas Anda adalah menjawab pertanyaan pengguna secara akurat dan informatif HANYA berdasarkan informasi dari "Konteks Dokumen" yang diberikan.

        Ikuti langkah-langkah berpikir berikut untuk menyusun jawaban Anda:

        **Langkah 1: Analisis & Ekstraksi Fakta.**
        - Baca pertanyaan pengguna dengan saksama: "{query}"
        - Baca setiap potongan informasi di dalam "Konteks Dokumen" di bawah ini.
        - Dari konteks tersebut, identifikasi dan catat semua fakta, poin kunci, nama, tanggal, atau data yang secara langsung relevan dengan pertanyaan pengguna.
        - Abaikan informasi apa pun dalam konteks yang tidak berhubungan dengan pertanyaan.

        **Langkah 2: Sintesis & Penulisan Jawaban.**
        - Berdasarkan semua fakta relevan yang telah Anda ekstrak pada Langkah 1, susunlah sebuah jawaban yang koheren, jelas, dan mudah dipahami dalam Bahasa Indonesia.
        - Jawaban akhir harus secara langsung menjawab pertanyaan pengguna dan tidak boleh mengandung informasi dari luar konteks yang diberikan.
        - Jika setelah menganalisis semua konteks tidak ada informasi yang cukup untuk menjawab pertanyaan, nyatakan dengan sopan bahwa Anda tidak memiliki informasi yang cukup.
        - Jangan menyebutkan proses berpikir Anda atau "Langkah 1 / Langkah 2" dalam jawaban akhir.

        **Konteks Dokumen:**
        ---
        {combined_context}
        ---

        **Pertanyaan Pengguna:**
        "{query}"

        Sekarang, berikan jawaban akhir yang sudah Anda sintesis.
        """
        
        try:
            # Melakukan panggilan POST ke API OpenRouter menggunakan pustaka requests
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": settings.HTTP_REFERER, 
                    "X-Title": "Chatbot FTMM"
                },
                data=json.dumps({
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [
                        {"role": "system", "content": "Anda adalah asisten AI yang ahli dalam menganalisis teks dan merangkum informasi secara akurat."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.5
                })
            )

            # Memeriksa apakah request berhasil
            response.raise_for_status()
            
            # Mengambil data JSON dari respons
            response_data = response.json()
            
            # Mengambil konten teks dari jawaban pertama
            return response_data['choices'][0]['message']['content'].strip()
        
        except requests.exceptions.RequestException as e:
            # Menangani semua error yang berhubungan dengan koneksi atau request
            print(f"Error dalam pemanggilan API OpenRouter: {e}")
            return "Maaf, terjadi kesalahan dalam memproses pertanyaan Anda."
        except (KeyError, IndexError) as e:
            # Menangani error jika struktur JSON dari respons tidak seperti yang diharapkan
            print(f"Error parsing respons dari OpenRouter: {e}")
            print(f"Response Body: {response.text}")
            return "Maaf, terjadi kesalahan dalam memproses respons dari server."

