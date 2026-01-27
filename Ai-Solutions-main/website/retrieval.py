# website/retrieval.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .cisg_docs import cisg_docs

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

doc_texts = [d["text"] for d in cisg_docs]
doc_embeddings = embed_model.encode(doc_texts)

index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(np.array(doc_embeddings))

def retrieve_cisg_context(query, k=5):
    q_vec = embed_model.encode([query])
    D, I = index.search(np.array(q_vec), k)
    retrieved = [cisg_docs[i]["text"] for i in I[0]]
    return "\n\n---\n\n".join(retrieved)