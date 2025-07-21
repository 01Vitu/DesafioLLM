# src/extract_content.py
import os
import fitz  # PyMuPDF
import easyocr
import pandas as pd

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text.strip()

def extract_table_to_csv(image_path, output_csv):
    reader = easyocr.Reader(['pt'], gpu=False)
    results = reader.readtext(image_path, detail=1)

    lines = {}
    for (bbox, text, prob) in results:
        y = round((bbox[0][1] + bbox[2][1]) / 2 / 15) * 15
        if y not in lines:
            lines[y] = []
        lines[y].append(text)

    sorted_lines = [lines[k] for k in sorted(lines.keys())]
    df = pd.DataFrame(sorted_lines)
    df.to_csv(output_csv, index=False, header=False, encoding='utf-8')

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    out_dir = os.path.join(base_dir, "data", "processed", "extracted_texts")
    os.makedirs(out_dir, exist_ok=True)

    pdf_file = os.path.join(raw_dir, "CÓDIGO DE OBRAS.pdf")
    image_file = os.path.join(raw_dir, "tabela.png")

    # Extrai PDF
    print("Extraindo texto do PDF...")
    txt = extract_pdf_text(pdf_file)
    with open(os.path.join(out_dir, "codigo_obras.txt"), "w", encoding="utf-8") as f:
        f.write(txt)

    # Extrai tabela
    print("Extraindo tabela da imagem...")
    csv_file = os.path.join(out_dir, "tabela_precos_bruta.csv")
    extract_table_to_csv(image_file, csv_file)

    print("Extração concluída!")