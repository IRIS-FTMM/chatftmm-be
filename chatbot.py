# chatbot.py
from retrieval import search_documents_bm25l
from summarization import Summarizer
from model_service import DF_KONTEKS, BM25L_MODEL, DF_DATASET
import pandas as pd

summarizer = Summarizer()

def get_chatbot_response(query: str) -> str:
    """Proses query dari pengguna dan kembalikan jawaban dari chatbot."""
    if not query.strip():
        return "Pertanyaan tidak boleh kosong."

    try:
        # Tahap 1: Retrieval Dokumen
        retrieved_docs = search_documents_bm25l(query, DF_KONTEKS, BM25L_MODEL, top_k=5)
        doc_indices = retrieved_docs['Index'].tolist()

        if not doc_indices:
             return "Maaf, saya tidak dapat menemukan informasi yang relevan dengan pertanyaan Anda."

        # Tahap 2: Pengumpulan Konteks dari Dataset Lengkap
        contexts = []
        for idx in doc_indices:
            # Cari baris yang cocok di DF_DATASET
            matching_row = DF_DATASET[DF_DATASET['Index'] == idx]
            if not matching_row.empty:
                # Ambil teks dari kolom 'Preprocessed Isi File'
                context_text = matching_row['Preprocessed Isi File'].values[0]
                if pd.notna(context_text):
                    contexts.append(str(context_text))

        if not contexts:
            return "Maaf, saya tidak dapat menemukan informasi yang relevan dengan pertanyaan Anda."

        # Tahap 3: Summarization
        summary = summarizer.summarize(query, contexts)
        return summary

    except Exception as e:
        print(f"Terjadi kesalahan pada alur chatbot: {e}")
        return "Maaf, terjadi kesalahan internal saat memproses permintaan Anda."