# src/semantic_search.py

import os
import requests
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# Load config.yaml
cfg = yaml.safe_load(Path("config.yaml").read_text())

API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
USER_AGENT = os.getenv("USER_AGENT")
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_papers(query: str, limit: int = 10):
    """
    Search Semantic Scholar for papers based on a query string.
    Returns list of paper metadata dictionaries.
    """

    headers = {
    "User-Agent": USER_AGENT
}


    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,authors,abstract,url,openAccessPdf"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    data = response.json()
    return data.get("data", [])
