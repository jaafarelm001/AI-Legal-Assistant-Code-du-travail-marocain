# 1️⃣ Imports
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os

# 2️⃣ Initialisation app
app = FastAPI(title="Assistant Juridique – Code du travail marocain")

# 3️⃣ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4️⃣ OpenAI (OPTIONNEL)
USE_LLM = False
client = None

try:
    from openai import OpenAI
    api_key = os.getenv("Clé_API")
    if api_key:
        client = OpenAI(api_key=api_key)
        USE_LLM = True
except Exception:
    USE_LLM = False

# 5️⃣ Chargement des données
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "data" / "processed" / "code_travail_enriched.json", encoding="utf-8") as f:
    articles = json.load(f)

index = faiss.read_index(
    str(BASE_DIR / "data" / "processed" / "faiss_index.index")
)

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# 6️⃣ Modèle de requête
class Question(BaseModel):
    question: str

# 7️⃣ Fonction de reformulation (ROBUSTE)
def reformulate_with_llm(question, articles):
    # 🔁 FALLBACK PAR DÉFAUT
    fallback = (
        "La loi encadre la relation de travail. "
        "Veuillez consulter les articles ci-dessous pour plus de détails."
    )

    if not USE_LLM or client is None:
        return fallback

    try:
        context = "\n\n".join(
            [f"{a.get('article')} : {a.get('texte')}" for a in articles if a.get("texte")]
        )

        prompt = f"""
Tu es un assistant juridique.
Ta mission est UNIQUEMENT de reformuler la réponse de manière simple.
Tu n’as PAS le droit d’interpréter la loi ni d’ajouter des informations.

Question :
{question}

Articles de loi :
{context}

Consigne :
- Réponds en une ou deux phrases maximum
- Utilise un langage simple
- Dis clairement si c’est autorisé ou interdit
- N’ajoute rien qui ne figure pas dans les articles
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return fallback

# 8️⃣ Endpoint /ask
@app.post("/ask")
def ask(q: Question):
    expanded_question = f"""
    {q.question}
    travail forcé
    licenciement
    préavis
    congés payés
    """

    q_embedding = model.encode([expanded_question])
    k = 3
    _, indices = index.search(q_embedding, k)

    results = []
    for i in indices[0]:
        art = articles[i]
        results.append({
            "article": art.get("article"),
            "texte": art.get("texte")
        })

    clear_answer = reformulate_with_llm(q.question, results)

    return {
        "question": q.question,
        "reponse_claire": clear_answer,
        "resultats": results,
        "disclaimer": "Cette information est fournie à titre indicatif et ne remplace pas une consultation juridique."
    }
