# src/query_answer.py
import os
import faiss
import numpy as np
import pickle
import subprocess
import sys
import re

def find_relevant_chunks(chunks, question_lower):
    """Busca chunks relevantes por busca semântica + regras"""
    relevant_texts = []

    # === 1. Busca semântica (FAISS) ===
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    q_emb = model.encode([question_lower]).astype("float32")

    _, indices = index.search(q_emb, k=3)
    for i in indices[0]:
        if i < len(chunks):
            text = chunks[i]["text"]
            if text not in relevant_texts:
                relevant_texts.append(text)

    # === 2. Busca ativa por artigos-chave ===
    if any(kw in question_lower for kw in ["recuo", "frente", "painel", "publicitário", "out-door", "anúncio"]):
        for chunk in chunks:
            if "Art. 241" in chunk["text"] and "recuos de frente" in chunk["text"]:
                if chunk["text"] not in relevant_texts:
                    relevant_texts.append(chunk["text"])
                break

    return "\n\n---\n\n".join(relevant_texts)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python query_answer.py \"sua pergunta aqui\"")
        sys.exit(1)

    question = sys.argv[1]
    question_lower = question.lower()

    # Caminhos absolutos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chunks_path = os.path.join(base_dir, "data", "processed", "chunks", "all_chunks.pkl")
    index_path = os.path.join(base_dir, "data", "processed", "chunks", "faiss_index.bin")
    emb_path = os.path.join(base_dir, "data", "processed", "chunks", "embeddings.npy")

    # Carrega dados
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    global index
    index = faiss.read_index(index_path)

    # Gera contexto
    context = find_relevant_chunks(chunks, question_lower)

    # Prompt limpo
    prompt = f"""
Você é um assistente jurídico especializado em códigos de obras municipais.
Responda apenas com base no contexto fornecido.

Contexto:
{context}

Pergunta: {question}
Resposta (cite o artigo se possível):
"""

    print("Enviando ao LLaMA 3...\n")
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        response = result.stdout.strip()
        print("Resposta:\n", response)
    except Exception as e:
        print(f"[Erro] {str(e)}")