import os
import json
import re

INPUT_DIR = "data/extracted_text"
OUTPUT_DIR = "data/sections"

os.makedirs(OUTPUT_DIR, exist_ok=True)

SECTION_HEADERS = [
    "abstract",
    "introduction",
    "method",
    "methodology",
    "materials and methods",
    "results",
    "discussion",
    "conclusion"
]

def split_sections(text):
    text_lower = text.lower()
    positions = {}

    for header in SECTION_HEADERS:
        match = re.search(r"\n\s*" + header + r"\b", text_lower)
        if match:
            positions[header] = match.start()

    sorted_sections = sorted(positions.items(), key=lambda x: x[1])

    sections = {}

    for i, (section, start) in enumerate(sorted_sections):
        end = sorted_sections[i+1][1] if i+1 < len(sorted_sections) else len(text)
        sections[section] = text[start:end].strip()

    return sections

def main():
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(INPUT_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        sections = split_sections(text)

        out_file = filename.replace(".txt", ".json")
        out_path = os.path.join(OUTPUT_DIR, out_file)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2)

        print("Segmented:", out_file)

if __name__ == "__main__":
    main()
