
import joblib
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

FOUNDATION_DF = joblib.load("embeddings_foundation.joblib")
INTER_DF = joblib.load("embeddings_Intermediate.joblib")
FINAL_DF = joblib.load("embeddings_Final.joblib")


def embed_query(text):
    r = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "bge-m3",
        "prompt": text
    })
    data = r.json()
    if "embedding" not in data:
        raise Exception(f"Embedding failed: {data}")
    return data["embedding"]


def search_rag(question, top_k=5):
    q_vec = embed_query(question)

    
    df = joblib.load("embeddings_foundation.joblib")
    df = df._append(joblib.load("embeddings_Intermediate.joblib"))
    df = df._append(joblib.load("embeddings_Final.joblib"))

    vectors = np.vstack(df["embedding"].values)
    sims = cosine_similarity(vectors, [q_vec]).flatten()

    top_idx = sims.argsort()[::-1][:top_k]
    return df.iloc[top_idx]
