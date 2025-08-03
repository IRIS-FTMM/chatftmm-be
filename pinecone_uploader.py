import os
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from pinecone_text.sparse import BM25Encoder
from tqdm.auto import tqdm # Untuk progress bar yang cantik

# ===============================================================
# KONFIGURASI
# ===============================================================
# Muat variabel dari file .env (SANGAT DISARANKAN)
load_dotenv()

# Kunci API dan Konfigurasi Pinecone & OpenAI
# Pastikan Anda sudah membuat file .env dan mengisinya
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Konfigurasi Index Pinecone
PINECONE_INDEX_NAME = "ftmm-unair-chatbot" # Anda bisa ganti nama ini
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSION = 3072 # Dimensi untuk model 'text-embedding-3-large'

# Path ke dataset Anda
DATASET_PATH = os.path.join("data", "Dataset_Optimized_FTMM_UNAIR.xlsx")

# Ukuran batch untuk upload
BATCH_SIZE = 100

def main():
    """
    Script utama untuk memproses dataset Excel, membuat embeddings,
    dan mengunggahnya ke Pinecone untuk Hybrid Search.
    """
    print("🚀 Memulai proses unggah data ke Pinecone...")

    # --- 1. Validasi dan Inisialisasi Klien ---
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        print("❌ KESALAHAN: Pastikan variabel PINECONE_API_KEY dan OPENAI_API_KEY sudah diatur dalam file .env Anda.")
        return

    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
        print("✅ Klien Pinecone dan OpenAI berhasil diinisialisasi.")
    except Exception as e:
        print(f"❌ Gagal menginisialisasi klien: {e}")
        return

    # --- 2. Muat Dataset dari Excel ---
    if not os.path.exists(DATASET_PATH):
        print(f"❌ KESALAHAN: File dataset tidak ditemukan di '{DATASET_PATH}'.")
        return
        
    print(f"[*] Memuat dataset dari '{DATASET_PATH}'...")
    df = pd.read_excel(DATASET_PATH)
    # Hapus baris yang tidak memiliki konteks pencarian
    df.dropna(subset=['konteks_pencarian'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f"✅ Berhasil memuat {len(df)} dokumen dari dataset.")

    # --- 3. Persiapan Index Pinecone ---
    print(f"[*] Memeriksa index Pinecone dengan nama '{PINECONE_INDEX_NAME}'...")
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        print(f"[*] Index tidak ditemukan. Membuat index baru...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="dotproduct", # Diperlukan untuk sparse vectors
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            }
        )
        print("✅ Index baru berhasil dibuat.")
    else:
        print("✅ Index sudah ada, akan digunakan.")
    
    index = pc.Index(PINECONE_INDEX_NAME)

    # --- 4. Persiapan Sparse Vector Encoder (BM25) ---
    print("[*] Mempersiapkan BM25 sparse encoder...")
    # 'corpus' adalah semua teks yang akan kita gunakan untuk 'melatih' model BM25
    corpus = df['konteks_pencarian'].tolist()
    
    bm25_encoder = BM25Encoder()
    print("[*] Melatih (fitting) BM25 encoder pada korpus data Anda. Ini mungkin butuh beberapa saat...")
    bm25_encoder.fit(corpus)
    print("✅ BM25 encoder berhasil dilatih.")
    
    # (Opsional) Simpan bobot BM25 untuk penggunaan di masa depan
    # bm25_encoder.dump("bm25_weights.json")

    # --- 5. Proses Batch Upload ke Pinecone ---
    print(f"\n[*] Memulai proses embedding dan upload ke Pinecone dalam batch berukuran {BATCH_SIZE}...")
    
    for i in tqdm(range(0, len(df), BATCH_SIZE)):
        i_end = min(i + BATCH_SIZE, len(df))
        batch = df.iloc[i:i_end]
        
        # Ambil teks untuk di-embed. Kita gunakan 'konteks_pencarian'
        texts_to_embed = batch['konteks_pencarian'].tolist()
        
        # Buat dense vectors (embeddings)
        dense_embeds = embeddings.embed_documents(texts_to_embed)
        
        # Buat sparse vectors (BM25)
        sparse_embeds = bm25_encoder.encode_documents(texts_to_embed)
        
        # Siapkan metadata. Kita simpan konten asli, judul, dan sumber
        metadata = batch[['Isi File', 'Judul', 'Sumber']].to_dict('records')
        
        # Buat ID unik untuk setiap dokumen
        ids = [str(idx) for idx in batch.index]
        
        # Gabungkan semuanya untuk di-upload
        vectors_to_upsert = []
        for doc_id, sparse, dense, meta in zip(ids, sparse_embeds, dense_embeds, metadata):
            vectors_to_upsert.append({
                'id': doc_id,
                'sparse_values': sparse,
                'values': dense,
                'metadata': meta
            })
            
        # Upload batch ke Pinecone
        index.upsert(vectors=vectors_to_upsert)

    print("\n🎉 Proses upload selesai!")
    print(f"[*] Mengecek statistik index...")
    stats = index.describe_index_stats()
    print(stats)
    print(f"✅ Berhasil! {stats.total_vector_count} vektor sekarang ada di index '{PINECONE_INDEX_NAME}'.")

if __name__ == "__main__":
    main()