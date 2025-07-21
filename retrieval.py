import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Fungsi Preprocessing untuk teks
def preprocess_text(text):
    # Pastikan input adalah string
    if not isinstance(text, str):
        text = str(text)

    # Lowercase semua teks
    text = text.lower()

    # Hapus karakter khusus dan angka
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)

    # Tokenisasi dan hapus stopwords
    stop_words = set(stopwords.words('indonesian'))
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]

    # Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = ' '.join(tokens)
    text = stemmer.stem(text)

    return text

# Class BM25L untuk pencarian dokumen
class BM25L:
    def __init__(self, corpus, k1=1.5, b=0.75, delta=1):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.delta = delta
        self.doc_lengths = [len(doc.split()) for doc in corpus]
        self.avg_doc_length = np.mean(self.doc_lengths) if self.doc_lengths else 0
        self.tf, self.idf = self._compute_tf_idf()

    def _compute_tf_idf(self):
        tf = {}
        idf = {}
        doc_term_counts = {}

        for doc_idx, doc in enumerate(self.corpus):
            terms = doc.split()
            unique_terms = set(terms)
            doc_tf = {term: terms.count(term) for term in unique_terms}
            tf[doc_idx] = doc_tf
            for term in unique_terms:
                doc_term_counts[term] = doc_term_counts.get(term, 0) + 1
        
        total_docs = len(self.corpus)
        for term, doc_count in doc_term_counts.items():
            idf[term] = np.log((total_docs - doc_count + 0.5) / (doc_count + 0.5) + 1)
        
        return tf, idf

    def get_score(self, query):
        query_terms = query.split()
        scores = []
        
        for doc_idx, doc_length in enumerate(self.doc_lengths):
            score = 0
            for term in query_terms:
                tf = self.tf[doc_idx].get(term, 0)
                L = 1 - self.b + self.b * (doc_length / self.avg_doc_length) if self.avg_doc_length > 0 else 1
                term_score = self.idf.get(term, 0) * ((tf * (self.k1 + 1)) / (tf + self.k1 * L) + self.delta)
                score += term_score
            scores.append(score)
        
        return np.array(scores)

def search_documents_bm25l(query, df, bm25l, top_k=5):
    """
    Cari dokumen yang relevan berdasarkan query menggunakan BM25L
    """
    processed_query = preprocess_text(query)
    bm25l_scores = bm25l.get_score(processed_query)

    # Ambil top k dokumen berdasarkan skor BM25L
    top_indices = bm25l_scores.argsort()[-top_k:][::-1]

    results = df.iloc[top_indices][['Index', 'konteks_pencarian']].copy()
    results['BM25L Score'] = bm25l_scores[top_indices]

    return results
