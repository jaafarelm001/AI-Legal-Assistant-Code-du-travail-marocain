import re, json

with open("data/raw/code_travail_clean.txt", encoding="utf-8") as f:
    text = f.read()

pattern = r"(Article\s+\d+)"
parts = re.split(pattern, text)

articles = []

for i in range(1, len(parts), 2):
    article_num = parts[i]
    article_text = parts[i+1].strip()

    articles.append({
        "code": "Code du travail marocain",
        "article": article_num,
        "texte": article_text
    })

with open("data/processed/code_travail.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"{len(articles)} articles extraits")
