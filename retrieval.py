# ===================================================================
# File: retrieval.py (VERSI OPTIMASI)
# Perubahan: Menggunakan kolom 'konteks_pencarian' untuk preprocessing.
# ===================================================================
import re
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Dictionaries dan Class BM25L tetap sama...
sinonim_dict = { "sdgs": ["sdg", "sdgs", "energi terbarukan", "energi bersih", "teknologi hijau", "energi berkelanjutan", "energi hijau", "tujuan pembangunan berkelanjutan", "sustainable development goals", "energi ramah lingkungan", "enerthi alternatif", "renewable energy"], "prestasi": ["penghargaan", "kejuaraan", "pencapaian"], "ospek": ["orientasi", "pkkmb", "masa pengenalan"], "jurusan": ["program studi", "prodi"], "kolaborasi": ["kerja sama", "partnership", "kolaborasi penelitian"], "industri": ["perusahaan", "sektor bisnis", "pihak luar"], "inovasi": ["produk inovatif", "karya inovatif", "ide baru"], "laboratorium": ["lab", "fasilitas penelitian"], "pariwisata": ["industri wisata", "sektor wisata", "tourism"], "ai": ["kecerdasan buatan", "artificial intelligence"], "kompetisi": ["lomba", "pertandingan", "kontes"], "organisasi": ["ormawa", "organisasi mahasiswa", "himpunan mahasiswa"], "benchmark": ["studi banding", "perbandingan", "acuan"], "desain": ["perancangan", "pengembangan", "rancangan"], "evos": ["electric vehicle operating system", "tim evos"], "kegiatan": ["program", "aktivitas", "event"], "summer program": ["program musim panas", "pertukaran pelajar", "outbond"], "artikel": ["berita", "publikasi", "tulisan"], "dekanat": ["pimpinan fakultas", "jajaran dekan", "dekan"], "imercy": ["bso imercy", "badan semi otonom imercy", "imercy ftmm"], "airfeel": ["teknologi airfeel", "inovasi airfeel", "produk airfeel"], "nuswantara garden": ["taman nuswantara", "proyek nuswantara", "nuswantara"], "industrial cup": ["kompetisi teknik industri", "lomba industrial cup", "event industrial cup"], "icatam": ["konferensi icatam", "seminar icatam", "event icatam"], "iot": ["internet of things", "teknologi iot", "penerapan iot"], "green cloud": ["cloud computing hijau", "teknologi ramah lingkungan", "komputasi awan hijau"], "desa binaan": ["program desa binaan", "desa ftmm"], "produk": ["inovasi", "hasil karya", "karya mahasiswa"], "msib": ["magang bersertifikat", "kampus merdeka", "program merdeka belajar"]}
prodi_dict = { 'tsd': 'teknologi sains data', 'ti': 'teknik industri', 'rn': 'rekayasa nanoteknologi', 'trkb': 'teknik robotika dan kecerdasan buatan', 'te': 'teknik elektro', 'fakultas teknologi maju dan multidisiplin': 'ftmm', 'fakultas teknologi maju multidisiplin': 'ftmm', 'fakultas teknologi maju': 'ftmm', 'universitas airlangga': 'unair'}
class BM25L:
    def __init__(self, corpus, k1=1.5, b=0.75, delta=1.0):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.delta = delta
        self.doc_lengths = [len(doc.split()) for doc in corpus]
        self.avg_doc_length = np.mean(self.doc_lengths) if self.doc_lengths else 0
        self.tf, self.idf = self._compute_tf_idf()
    def _compute_tf_idf(self):
        tf, idf, doc_term_counts = {}, {}, {}
        for doc_idx, doc in enumerate(self.corpus):
            terms = doc.split()
            unique_terms = set(terms)
            doc_tf = {term: terms.count(term) for term in unique_terms}
            tf[doc_idx] = doc_tf
            for term in unique_terms:
                doc_term_counts[term] = doc_term_counts.get(term, 0) + 1
        total_docs = len(self.corpus)
        for term, doc_count in doc_term_counts.items():
            idf[term] = np.log((total_docs - doc_count + 0.5) / (doc_count + 0.5) + 1.0)
        return tf, idf
    def get_score(self, query):
        query_terms = query.split()
        scores = np.zeros(len(self.corpus))
        for i, doc_len in enumerate(self.doc_lengths):
            doc_score = 0
            for term in query_terms:
                if term in self.idf:
                    tf_val = self.tf[i].get(term, 0)
                    numerator = tf_val * (self.k1 + 1)
                    denominator = tf_val + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_length)
                    term_score = self.idf[term] * (numerator / denominator + self.delta)
                    doc_score += term_score
            scores[i] = doc_score
        return scores
def preprocess_text(text):
    if not isinstance(text, str): text = str(text)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text_lower = text.lower()
    for key, synonyms in sinonim_dict.items():
        for synonym in synonyms:
            pattern = r'\b' + re.escape(synonym.lower()) + r'\b'
            text_lower = re.sub(pattern, key, text_lower)
    for abbr, full in prodi_dict.items():
        text_lower = re.sub(r'\b' + abbr + r'\b', full, text_lower)
    text = re.sub(r'[^\w\s]', ' ', text_lower)
    text = re.sub(r'\d+', ' ', text)
    text = ' '.join(text.split())
    stop_words = set(stopwords.words('indonesian'))
    tokens = [token for token in word_tokenize(text) if token not in stop_words]
    return stemmer.stem(' '.join(tokens))

def create_bm25l_retrieval_system(data_path):
    try:
        df = pd.read_excel(data_path)
        # --- PERUBAHAN DI SINI ---
        # Kita sekarang memproses kolom 'konteks_pencarian' yang sudah dioptimalkan
        if 'konteks_pencarian' not in df.columns:
            raise ValueError("File dataset harus memiliki kolom 'konteks_pencarian'")
        
        print("Memulai preprocessing teks untuk model retrieval...")
        df['preprocessed_text'] = df['konteks_pencarian'].apply(preprocess_text)
        print("Preprocessing selesai.")
        # --- AKHIR PERUBAHAN ---

        bm25l = BM25L(df['preprocessed_text'].tolist())
        return df, bm25l
    except Exception as e:
        print(f"Error creating retrieval system: {e}")
        return None, None

def search_documents_bm25l(query, df, bm25l, top_k=5):
    processed_query = preprocess_text(query)
    bm25l_scores = bm25l.get_score(processed_query)
    top_indices = np.nan_to_num(bm25l_scores).argsort()[-top_k:][::-1]
    results = df.iloc[top_indices].copy()
    results['BM25L_Score'] = bm25l_scores[top_indices]
    return results