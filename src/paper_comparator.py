import json
import re

# -------- PATHS --------
FINDINGS_FILE = "data/analysis/findings.json"
OUTPUT_FILE = "data/analysis/comparison.json"

# -------- KEYWORD MAP FOR CLASSIFICATION --------
INCREASE_WORDS = [
    "increase", "increased", "improve", "improved", "acceptance",
    "higher", "better", "positive", "uptake", "will accept"
]

DECREASE_WORDS = [
    "decrease", "decreased", "reduced", "reduction", "lower",
    "decline", "dropped"
]

RISK_WORDS = [
    "risk", "odds ratio", "or =", "hesitancy", "mortality",
    "vulnerable", "associated", "association"
]

# -------- CLASSIFICATION FUNCTION --------
def classify_sentence(sentence):
    s = sentence.lower()

    # risk first (highest priority)
    for word in RISK_WORDS:
        if word in s:
            return "risk"

    for word in DECREASE_WORDS:
        if word in s:
            return "decrease"

    for word in INCREASE_WORDS:
        if word in s:
            return "increase"

    return "neutral"

# -------- LOAD FINDINGS --------
with open(FINDINGS_FILE, "r", encoding="utf-8") as f:
    findings = json.load(f)

# -------- GROUP ACROSS PAPERS --------
comparison = {
    "increase": [],
    "decrease": [],
    "risk": [],
    "neutral": []
}

for paper, sentences in findings.items():
    for sentence in sentences:
        category = classify_sentence(sentence)

        comparison[category].append({
            "paper": paper,
            "sentence": sentence
        })

# -------- SAVE OUTPUT --------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(comparison, f, indent=2)

print("✅ Cross-paper comparison completed.")
print(f"📁 Output saved to: {OUTPUT_FILE}")
