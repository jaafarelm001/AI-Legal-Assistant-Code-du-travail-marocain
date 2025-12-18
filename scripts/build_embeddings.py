import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "data" / "processed" / "code_travail_enriched.json"

with open(data_path, encoding="utf-8") as f:
    articles = json.load(f)

# Texte à vectoriser
texts = [
    f"""
    {art.get('article', '')}
    {art.get('titre', '')}
    {art.get('texte', '')}
    {' '.join(art.get('mots_cles', []))}
    """
    for art in articles
]




# Modèle d'embedding
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Création des embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# Sauvegarde
np.save(BASE_DIR / "data" / "processed" / "embeddings.npy", embeddings)

print("✅ Embeddings créés")
print("Shape :", embeddings.shape)
