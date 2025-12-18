import json
from pathlib import Path

path = Path("data/processed/code_travail_enriched.json")

with open(path, encoding="utf-8") as f:
    articles = json.load(f)

print("✅ Dataset chargé")
print("Nombre d’articles :", len(articles))
print("Exemple :", articles[0]["article"])
