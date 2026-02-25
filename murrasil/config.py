import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", "15"))
MAX_NEWS_AGE_HOURS = int(os.getenv("MAX_NEWS_AGE_HOURS", "48"))
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
