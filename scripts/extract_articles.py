import pdfplumber

pdf_path = "data/raw/code_travail.pdf"
output_txt = "data/raw/code_travail.txt"

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

with open(output_txt, "w", encoding="utf-8") as f:
    f.write(full_text)

print("Extraction terminée")
