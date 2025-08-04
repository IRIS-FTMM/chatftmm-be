import traceback
from retrieval import search_documents_bm25l
from summarization import Summarizer
import model_service
from typing import List, Dict, Any, Optional

summarizer = Summarizer()

# --- NEW: Dictionary for handling simple greetings and small talk ---
small_talk_responses = {
    "halo": "Halo! Ada yang bisa saya bantu seputar FTMM?",
    "hai": "Hai! Ada yang bisa saya bantu seputar FTMM?",
    "terima kasih": "Sama-sama! Senang bisa membantu. Apakah ada pertanyaan lain?",
    "makasih": "Sama-sama! Senang bisa membantu. Apakah ada pertanyaan lain?",
    "apa kabar": "Kabar baik, terima kasih! Saya siap membantu Anda dengan informasi seputar FTMM.",
    "apa kabarmu": "Kabar baik, terima kasih! Saya siap membantu Anda dengan informasi seputar FTMM."
}

def perbaiki_gelar_umum(text: str) -> str:
    # ... (This function remains unchanged)
    perbaikan = {
        "Prof Dwi Setyawan SSi MSi Apt": "Prof. Dr. Dwi Setyawan, S.Si., M.Si., Apt.",
        "Prof Dwi Setyawan": "Prof. Dr. Dwi Setyawan, S.Si., M.Si., Apt.",
        "SSi": "S.Si.", "MSi": "M.Si.", " PhD": ", Ph.D.",
    }
    for salah, benar in perbaikan.items():
        text = text.replace(salah, benar)
    return text

# --- MODIFIED: Function signature updated to accept history ---
def get_chatbot_response(query: str, history: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Menjalankan alur kerja RAG lengkap, dari pencarian hingga post-processing.
    """
    if not query.strip():
        return "Pertanyaan tidak boleh kosong."

    # --- NEW: Check for small talk first ---
    cleaned_query = query.strip().lower()
    if cleaned_query in small_talk_responses:
        return small_talk_responses[cleaned_query]

    # If not small talk, proceed with the RAG pipeline
    try:
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

        # --- MODIFIED: Pass history to the summarizer ---
        print("Mengirim konteks dan riwayat ke AI untuk diringkas...")
        summary = summarizer.summarize(query, contexts, history)
        
        print("Melakukan perbaikan format akhir pada jawaban...")
        final_summary = perbaiki_gelar_umum(summary)

        return final_summary

    except Exception as e:
        print(f"Terjadi kesalahan fatal pada alur chatbot: {e}")
        traceback.print_exc()
        return "Maaf, terjadi kesalahan internal yang tidak terduga."