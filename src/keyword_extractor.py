import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer

# --------- PATHS (Step B) ---------
SECTIONS_DIR = "data/sections"
OUTPUT_FILE = "data/analysis/keywords.json"

# --------- READ SECTION FILES ---------
documents = []
paper_names = []

for filename in os.listdir(SECTIONS_DIR):
    if filename.endswith(".json"):
        file_path = os.path.join(SECTIONS_DIR, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Take only important sections
        abstract = data.get("abstract", "")
        results = data.get("results", "")
        conclusion = data.get("conclusion", "")

        combined_text = f"{abstract} {results} {conclusion}"

        documents.append(combined_text)
        paper_names.append(filename.replace(".json", ""))

# --------- APPLY TF-IDF ---------
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10
)

tfidf_matrix = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

# --------- EXTRACT KEYWORDS ---------
keywords_per_paper = {}

for idx, paper in enumerate(paper_names):
    scores = tfidf_matrix[idx].toarray()[0]
    top_indices = scores.argsort()[::-1]

    keywords = [feature_names[i] for i in top_indices if scores[i] > 0]
    keywords_per_paper[paper] = keywords

# --------- SAVE OUTPUT ---------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(keywords_per_paper, f, indent=2)

print("✅ TF-IDF keyword extraction completed.")
print(f"📁 Output saved to: {OUTPUT_FILE}")
