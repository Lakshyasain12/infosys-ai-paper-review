# debug_env.py
import os
from dotenv import load_dotenv

load_dotenv()

k = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
u = os.getenv("USER_AGENT")

print("API key present?:", bool(k))
print("API key startswith 'sk_'?:", str(k).startswith("sk_") if k else False)
print("USER_AGENT present?:", bool(u))
print("USER_AGENT value:", u)
