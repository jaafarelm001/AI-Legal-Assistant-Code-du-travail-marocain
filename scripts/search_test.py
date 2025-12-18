import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

# Charger articles
with open(
    BASE_DIR / "data" / "processed" / "code_travail_enriched.json",
    encoding="utf-8"
) as f:
    articles = json.load(f)

# Charger index FAISS
index = faiss.read_index(
    str(BASE_DIR / "data" / "processed" / "faiss_index.index")
)

# Charger modèle d’embeddings
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Question utilisateur
question = """
Un employeur peut-il forcer un salarié à travailler ?
travail forcé
contre la volonté du salarié
réquisition du salarié
liberté du travail
"""


# Vectoriser la question
q_embedding = model.encode([question])

# Recherche des k articles les plus proches
k = 3
distances, indices = index.search(q_embedding, k)

print("\n🔍 Résultats trouvés :\n")

print("\n🔍 Résultats trouvés :\n")

for i in indices[0]:
    art = articles[i]
    article_num = art.get("article", "Article inconnu")
    texte = art.get("texte", "[Texte indisponible]")
    print(f"{article_num} → {texte}\n")

