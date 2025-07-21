# file: chatbot.py (DENGAN POST-PROCESSING)

import traceback
from retrieval import search_documents_bm25l
from summarization import Summarizer
import model_service

# Inisialisasi summarizer sekali saja
summarizer = Summarizer()

# --- FUNGSI BARU UNTUK MEMPERBAIKI KESALAHAN UMUM ---
def perbaiki_gelar_umum(text: str) -> str:
    """
    Fungsi ini secara paksa memperbaiki kesalahan format gelar yang sering dilakukan AI.
    """
    perbaikan = {
        "Prof Dwi Setyawan SSi MSi Apt": "Prof. Dr. Dwi Setyawan, S.Si., M.Si., Apt.",
        "Prof Dwi Setyawan": "Prof. Dr. Dwi Setyawan, S.Si., M.Si., Apt.",
        # Tambahkan kesalahan umum lainnya di sini
        # Formatnya: "Teks Salah": "Teks Benar"
        "SSi": "S.Si.",
        "MSi": "M.Si.",
        " PhD": ", Ph.D.", # spasi di depan untuk menghindari kata 'phd' di tengah kalimat
    }
    
    for salah, benar in perbaikan.items():
        text = text.replace(salah, benar)
        
    return text
# ----------------------------------------------------


def get_chatbot_response(query: str) -> str:
    """
    Menjalankan alur kerja RAG lengkap, dari pencarian hingga post-processing.
    """
    if not query.strip():
        return "Pertanyaan tidak boleh kosong."

    try:
        # ... (Tahap 1 & 2: Retrieval & Konteks - TIDAK ADA PERUBAHAN)
        print(f"Mencari dokumen untuk: '{query}'")
        if model_service.BM25L_MODEL is None or model_service.DF_KONTEKS is None:
            return "Maaf, sistem chatbot belum siap."

        retrieved_docs = search_documents_bm25l(
            query,
            model_service.DF_KONTEKS,
            model_service.BM25L_MODEL,
            top_k=3
        )

        if retrieved_docs.empty:
            return "Maaf, saya tidak dapat menemukan informasi yang relevan."

        doc_indices = retrieved_docs.index.tolist()
        contexts = model_service.DF_DATASET.loc[doc_indices, 'Isi File'].dropna().tolist()

        if not contexts:
            return "Maaf, meskipun dokumen ditemukan, saya tidak bisa mengambil isinya."

        # Tahap 3: Summarization
        print("Mengirim konteks ke AI untuk diringkas...")
        summary = summarizer.summarize(query, contexts)
        
        # --- TAHAP 4 (BARU): POST-PROCESSING ---
        print("Melakukan perbaikan format akhir pada jawaban...")
        final_summary = perbaiki_gelar_umum(summary)
        # --------------------------------------

        # Mengembalikan hasil yang sudah final dan diperbaiki
        return final_summary

    except Exception as e:
        print(f"Terjadi kesalahan fatal pada alur chatbot: {e}")
        traceback.print_exc()
        return "Maaf, terjadi kesalahan internal yang tidak terduga."