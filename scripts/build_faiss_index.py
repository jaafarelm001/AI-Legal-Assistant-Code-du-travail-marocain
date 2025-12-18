import numpy as np
import faiss
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Charger les embeddings
embeddings = np.load(BASE_DIR / "data" / "processed" / "embeddings.npy")

dimension = embeddings.shape[1]

# Créer l’index FAISS
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Sauvegarder l’index
faiss.write_index(
    index,
    str(BASE_DIR / "data" / "processed" / "faiss_index.index")
)

print("✅ Index FAISS créé")
print("Nombre de vecteurs :", index.ntotal)
