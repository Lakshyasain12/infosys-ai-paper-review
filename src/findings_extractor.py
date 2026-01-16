import os
import json
import re

# -------- PATHS --------
SECTIONS_DIR = "data/sections"
OUTPUT_FILE = "data/analysis/findings.json"

# -------- RESULT VERBS (case-insensitive) --------
RESULT_VERBS = [
    "show", "shows", "showed",
    "indicate", "indicates", "indicated",
    "demonstrate", "demonstrates", "demonstrated",
    "significant", "significantly",
    "increase", "increased",
    "decrease", "decreased",
    "reduce", "reduced",
    "associated", "association",
    "odds ratio", "or ="
]

# -------- SIMPLE REGEX SENTENCE SPLITTER --------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

# -------- CHECK IF SENTENCE IS A KEY FINDING --------
def is_key_finding(sentence):
    sentence_lower = sentence.lower()

    # Rule 1: contains a number
    if re.search(r'\d', sentence):
        return True

    # Rule 2: contains result verb
    for verb in RESULT_VERBS:
        if verb in sentence_lower:
            return True

    return False

# -------- MAIN EXTRACTION --------
findings = {}

for filename in os.listdir(SECTIONS_DIR):
    if filename.endswith(".json"):
        file_path = os.path.join(SECTIONS_DIR, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        results_text = data.get("results", "")
        conclusion_text = data.get("conclusion", "")
        combined_text = f"{results_text} {conclusion_text}"

        sentences = split_sentences(combined_text)

        key_sentences = []
        for sentence in sentences:
            if is_key_finding(sentence):
                key_sentences.append(sentence)

        paper_name = filename.replace(".json", "")
        findings[paper_name] = key_sentences

# -------- SAVE OUTPUT --------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(findings, f, indent=2)

print("✅ Key-finding extraction completed.")
print(f"📁 Output saved to: {OUTPUT_FILE}")
