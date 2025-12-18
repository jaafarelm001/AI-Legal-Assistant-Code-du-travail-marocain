import json
from pathlib import Path

input_path = Path("data/processed/code_travail.json")
output_path = Path("data/processed/code_travail_enriched.json")

with open(input_path, encoding="utf-8") as f:
    articles = json.load(f)

enriched_articles = []

for art in articles:
    enriched_articles.append({
        "code": art.get("code", "Code du travail marocain"),
        "article": art.get("article"),
        "titre": "",
        "texte": art.get("texte"),
        "resume_simple": "",
        "categorie": "",
        "langue": "fr",
        "mots_cles": []
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(enriched_articles, f, ensure_ascii=False, indent=2)

print("✅ JSON enrichi créé :", output_path)
print("Nombre d’articles :", len(enriched_articles))
