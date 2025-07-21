# src/clean_table.py
import pandas as pd
import re
import os

print("🧹 Iniciando limpeza da tabela...")

# Caminhos
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bruto_csv = os.path.join(base_dir, "data", "processed", "extracted_texts", "tabela_precos_bruta.csv")
limpo_csv = os.path.join(base_dir, "data", "processed", "extracted_texts", "tabela_precos_limpa.csv")

# Verifica se o CSV bruto existe
if not os.path.exists(bruto_csv):
    print(f"Arquivo não encontrado: {bruto_csv}")
    exit(1)

# Carrega
df = pd.read_csv(bruto_csv, header=None)
lines = df.astype(str).apply(lambda row: ' '.join(row.dropna().tolist()), axis=1).tolist()

data = []
for line in lines:
    if len(line.strip()) < 5 or any(x in line.upper() for x in ["FERFISH", "TABELA", "EMAIL", "CONTRIBUINTE", "PARQUE", "TELEFONE"]):
        continue

    # Divide por múltiplos espaços ou vírgulas
    parts = re.split(r'\s{2,}|,', line)
    parts = [p.strip(' "()') for p in parts if p.strip()]

    if len(parts) < 2:
        continue

    # Identifica código
    codigo = parts[0] if re.match(r'^[A-Z0-9]{6,}', parts[0]) else ""

    # Preços
    precos = [re.sub(r'[^\d,\.]', '', p).replace(',', '.') for p in parts if re.search(r'\d+[,.]\d+', p)]
    preco_custo = precos[0] if len(precos) > 0 else ""
    preco_venda = precos[1] if len(precos) > 1 else ""

    # Descrição
    desc_parts = [p for p in parts if p not in precos and not re.match(r'^[A-Z0-9]{6,}', p)]
    descricao = " ".join(desc_parts)

    # Correções comuns
    correcoes = {
        "Dobradisa": "Dobradiça",
        "Paralusos": "Parafusos",
        "exlintor": "extintor",
        "exintor": "extintor",
        "siwples": "simples",
        "melal": "metal",
        "caixa /0O": "caixa 100",
        "caixa /00": "caixa 100",
        "aul": "galvanizado"
    }
    for errado, certo in correcoes.items():
        descricao = descricao.replace(errado, certo)

    data.append([codigo, descricao, preco_custo, preco_venda])

# Salva
df_clean = pd.DataFrame(data, columns=["codigo", "descricao", "preco_custo", "preco_venda"])
df_clean.to_csv(limpo_csv, index=False, encoding='utf-8')
print(f"Tabela limpa salva em: {limpo_csv}")
print("\nPrévia:")
print(df_clean.head())