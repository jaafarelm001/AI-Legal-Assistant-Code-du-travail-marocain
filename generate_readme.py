import json

with open("project_info.json", encoding="utf-8") as f:
    info = json.load(f)

readme = f"""
# ⚖️ {info['title']}

## 🎯 Description
{info['description']}

## 🧠 Fonctionnalités
""" + "\n".join([f"- {f}" for f in info["features"]]) + """

## 🛠️ Technologies utilisées
""" + "\n".join([f"- {t}" for t in info["technologies"]]) + f"""

## 👤 Auteur
{info['author']}

## ⚠️ Disclaimer
Les informations fournies sont à titre indicatif et ne remplacent pas une consultation juridique.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("✅ README.md généré automatiquement")
