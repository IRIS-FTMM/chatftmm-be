import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from pinecone_text.sparse import BM25Encoder
import pprint # Untuk membuat output lebih rapi

# ===============================================================
# KONFIGURASI (Sama seperti uploader)
# ===============================================================
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_INDEX_NAME = "ftmm-unair-chatbot"
EMBEDDING_MODEL = "text-embedding-3-large"

def main():
    """
    Script untuk melakukan query hybrid search ke Pinecone dan melihat hasilnya.
    """
    print("🚀 Memulai Pinecone Hybrid Search Tester...")

    # --- 1. Inisialisasi Klien ---
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        print("❌ KESALAHAN: Pastikan API keys sudah diatur dalam file .env.")
        return

    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
        bm25_encoder = BM25Encoder().default() # Gunakan default, tidak perlu fit untuk query
        index = pc.Index(PINECONE_INDEX_NAME)
        print("✅ Klien Pinecone dan OpenAI berhasil diinisialisasi.")
    except Exception as e:
        print(f"❌ Gagal menginisialisasi klien: {e}")
        return

    # --- 2. Loop untuk Menerima Input Query dari Pengguna ---
    while True:
        print("\n" + "="*50)
        query = input("❓ Masukkan pertanyaan Anda (atau ketik 'exit' untuk keluar): ")
        if query.lower() == 'exit':
            break

        print(f"\n🔍 Mencari untuk query: '{query}'")
        
        # --- 3. Buat Dense & Sparse Vector untuk Query ---
        # Dense vector dari OpenAI
        dense_vec = embeddings.embed_query(query)
        
        # Sparse vector dari BM25
        sparse_vec = bm25_encoder.encode_queries(query)
        
        # --- 4. Lakukan Query ke Pinecone ---
        try:
            # Lakukan hybrid search dengan menggabungkan dense dan sparse
            # Alpha=0.5 berarti kita memberi bobot seimbang antara pencarian semantik (dense) dan keyword (sparse)
            # Anda bisa mengubah nilai alpha (0.0 - 1.0) untuk melihat hasil yang berbeda
            result = index.query(
                vector=dense_vec,
                sparse_vector=sparse_vec,
                top_k=3,  # Ambil 3 hasil teratas
                include_metadata=True
            )
            
            # --- 5. Tampilkan Hasil ---
            print("\n✅ Hasil Pencarian Ditemukan:")
            print("-"*50)
            
            if result['matches']:
                for i, match in enumerate(result['matches']):
                    print(f"--- HASIL #{i+1} (Skor: {match['score']:.4f}) ---")
                    pprint.pprint(match['metadata']) # Tampilkan semua metadata
                    print("\n")
            else:
                print("Tidak ada hasil yang cocok ditemukan.")

        except Exception as e:
            print(f"❌ Terjadi kesalahan saat query: {e}")

    print("👋 Sampai jumpa!")

if __name__ == "__main__":
    main()