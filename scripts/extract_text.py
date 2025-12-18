import pdfplumber
from pathlib import Path

pdf_path = Path("data/raw/code_travail.pdf")
output_path = Path("data/raw/code_travail.txt")

full_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:  # 🔑 TRÈS IMPORTANT
            full_text += f"\n{text}"
        else:
            print(f"⚠️ Page {i+1} vide")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print("✅ Extraction terminée")
print("Nombre de caractères :", len(full_text))
