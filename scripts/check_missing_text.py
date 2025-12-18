import json
from pathlib import Path

path = Path("data/processed/code_travail_enriched.json")

with open(path, encoding="utf-8") as f:
    articles = json.load(f)

missing = []

for i, art in enumerate(articles):
    if "texte" not in art or not art["texte"].strip():
        missing.append((i, art.get("article", "inconnu")))

print("Articles sans texte :", len(missing))
for m in missing[:10]:
    print(m)
