import re

with open("data/raw/code_travail.txt", encoding="utf-8") as f:
    text = f.read()

# Supprimer espaces multiples
text = re.sub(r"\s+", " ", text)

# Supprimer numéros de page (exemple)
text = re.sub(r"Page\s+\d+", "", text)

with open("data/raw/code_travail_clean.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Nettoyage terminé")
