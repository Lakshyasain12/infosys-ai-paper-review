# src/config_test.py
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

# load .env
load_dotenv()

# read config.yaml
cfg_path = Path("config.yaml")
cfg = yaml.safe_load(cfg_path.read_text())

print("Default query:", cfg["search"]["default_query"])
print("Raw pdfs folder:", cfg["paths"]["raw_pdfs"])
print("SEMANTIC_SCHOLAR_API_KEY present?:", bool(os.getenv("SEMANTIC_SCHOLAR_API_KEY")))
