
# 🏗️ Desafio Técnico: Pipeline RAG com LLaMA 3  
**Sistema de Recuperação e Geração de Respostas com Base em Documentos Legais**

Solução funcional para indexar documentos heterogêneos (PDFs com ou sem texto e imagens), aplicar OCR, gerar base vetorial semântica e responder perguntas com LLM.

---

## 📌 Objetivo

Construir um pipeline que:
- ✅ Indexe documentos heterogêneos (PDFs, imagens)
- ✅ Aplique OCR em imagens e PDFs sem texto
- ✅ Gere uma base vetorial com embeddings semânticos
- ✅ Recupere informações relevantes por similaridade
- ✅ Utilize uma LLM (LLaMA 3 via Ollama) para responder perguntas com base nos documentos

---

## 🧩 Arquitetura do Pipeline

```
[Documentos PDF / Imagem]
             ↓
    extract_content.py  → Extração de conteúdo (PyMuPDF + EasyOCR)
             ↓
    clean_table.py      → Limpeza de tabelas OCR extraídas
             ↓
    chunk_and_embed.py  → Chunking jurídico + embeddings semânticos
             ↓
    vector_store.py     → Construção do índice vetorial (FAISS)
             ↓
    query_answer.py     → Busca semântica + resposta via LLaMA 3
             ↓
[Resposta em linguagem natural]
```

---

## 🧠 Diagrama Conceitual

```
+------------------+     +-------------------+
|   PDF / Imagem   | --> | Extração de Texto |
+------------------+     +-------------------+
                                ↓
                     +-----------------------+
                     | Chunking e Embeddings |
                     +-----------------------+
                                ↓
                      +--------------------+
                      | Banco Vetorial     |
                      |      (FAISS)       |
                      +--------------------+
                                ↓
                   +----------------------------+
                   | Recuperação Semântica      |
                   +----------------------------+
                                ↓
             +----------------------------------+
             | Geração de Resposta com LLaMA 3  |
             +----------------------------------+
```

---

## 📁 Estrutura de Pastas

```
TESTE_NUVEN/
├── data/
│   ├── raw/                    # Documentos originais
│   │   ├── CÓDIGO DE OBRAS.pdf
│   │   └── tabela.webp
│   └── processed/
│       ├── extracted_texts/    # Textos extraídos
│       │   ├── codigo_obras.txt
│       │   ├── tabela_precos_bruta.csv
│       │   └── tabela_precos_limpa.csv
│       └── chunks/             # Chunks e embeddings
│           ├── all_chunks.pkl
│           ├── embeddings.npy
│           └── faiss_index.bin
├── src/
│   ├── extract_content.py      # Extração de conteúdo OCR/textual
│   ├── clean_table.py          # Limpeza de tabelas OCR extraídas
│   ├── chunk_and_embed.py      # Divisão e vetorização de conteúdo
│   ├── vector_store.py         # Construção do índice FAISS
│   └── query_answer.py         # Recuperação + resposta com LLaMA 3
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este documento
```

---

## ⚙️ Como Executar

### 1. Pré-requisitos
- Python 3.9+
- [Ollama](https://ollama.com/) instalado e funcionando localmente
- Modelo LLaMA 3 baixado:

```bash
ollama pull llama3
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

> 💡 `easyocr` pode demorar um pouco na instalação inicial, pois baixa modelos de linguagem.

### 3. Executar o pipeline

```bash
cd TESTE_NUVEN

# 1. Extração de texto (OCR e PDFs)
python src/extract_content.py

# 2. Limpeza de tabelas OCR (CSV bruto → limpo)
python src/clean_table.py

# 3. Chunking jurídico + geração de embeddings
python src/chunk_and_embed.py

# 4. Construção do índice vetorial FAISS
python src/vector_store.py

# 5. Fazer uma pergunta!
python src/query_answer.py "Qual é o recuo frontal mínimo para painéis publicitários?"
```

---

## 💬 Exemplos de Perguntas

```bash
python src/query_answer.py "Qual é o recuo frontal mínimo para painéis publicitários?"
# → Resposta: 3,00m (Art. 241, alínea a)

python src/query_answer.py "Qual é o pé-direito mínimo para salas de aula?"
# → Resposta: 3,00m (§3º do Art. 67)

python src/query_answer.py "Quanto custa um parafuso cabeça hexagonal em aço?"
# → Resposta com base na tabela de preços

python src/query_answer.py "É permitido vender sorvetes ambulantes?"
# → Sim, conforme Art. 307
```

---

## 🧠 Justificativas Técnicas

### 1. Extração de Conteúdo
- **PyMuPDF**: Extração rápida e precisa de texto de PDFs com layout preservado.
- **EasyOCR**: OCR leve, multilíngue e eficaz para imagens e PDFs escaneados.
- Conversão automática de `.webp → .png` para compatibilidade OCR.

### 2. Chunking Jurídico Inteligente
- Quebra baseada em `Art.`, `§`, `Inciso`, mantendo coesão semântica.
- Ideal para legislação e documentos normativos — evita perda de contexto.

### 3. Embeddings Semânticos
- Modelo: `paraphrase-multilingual-MiniLM-L12-v2`
- Otimizado para português e tarefas de similaridade textual.
- Captura relações semânticas mesmo com vocabulário técnico-legal.

### 4. Armazenamento Vetorial
- **FAISS** (Facebook AI Similarity Search): rápido, local e escalável.
- Sem dependência de nuvem, ideal para ambientes sensíveis e privados.

### 5. Geração com LLaMA 3 via Ollama
- Roda localmente, sem custo.
- Alta qualidade de geração e compreensão legal.
- Instruções no prompt orientam o modelo a citar artigos quando aplicável.

### 6. Robustez na Recuperação
- Estratégia híbrida:
  - Busca semântica primária via embeddings
  - Fallback por palavra-chave quando necessário
- Reduz risco de respostas vazias ou irrelevantes.

---

## ✅ Resultados Esperados
- Pipeline completo e modular, pronto para uso e adaptação em ambientes jurídicos.
- Código legível, organizado e facilmente escalável.
- Respostas com base nos documentos fornecidos, com alto grau de precisão legal.
