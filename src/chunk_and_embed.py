# src/chunk_and_embed.py
import os
import pickle
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter

print("🔧 Iniciando chunking por artigos...")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
txt_file = os.path.join(base_dir, "data", "processed", "extracted_texts", "codigo_obras.txt")
out_dir = os.path.join(base_dir, "data", "processed", "chunks")
os.makedirs(out_dir, exist_ok=True)

if not os.path.exists(txt_file):
    print(f"Erro: {txt_file} não encontrado.")
    exit(1)

with open(txt_file, "r", encoding="utf-8") as f:
    text = f.read()

# Divide EXATAMENTE nos artigos e parágrafos
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\nArt\. \d+", "\n§", "\nParágrafo", "\.\n", "\n\n"]
)

chunks = splitter.split_text(text)
all_chunks = [{"source": "codigo_obras", "text": c} for c in chunks]

# Salva chunks
chunks_path = os.path.join(out_dir, "all_chunks.pkl")
with open(chunks_path, "wb") as f:
    pickle.dump(all_chunks, f)
print(f"{len(all_chunks)} chunks gerados.")

# Gera embeddings com modelo forte em português
print("🧠 Gerando embeddings com BERT multilíngue...")
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode([c["text"] for c in all_chunks], show_progress_bar=True)

np.save(os.path.join(out_dir, "embeddings.npy"), embeddings)
print("Embeddings salvos!")