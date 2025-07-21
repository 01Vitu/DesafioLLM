# src/vector_store.py
import faiss
import numpy as np
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
emb_path = os.path.join(base_dir, "data", "processed", "chunks", "embeddings.npy")
index_path = os.path.join(base_dir, "data", "processed", "chunks", "faiss_index.bin")

embeddings = np.load(emb_path).astype("float32")
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, index_path)
print(f"Índice vetorial criado em: {index_path}")