import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "soft_corner_docs")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    TOP_K = int(os.getenv("TOP_K", "6"))
    MIN_SCORE = float(os.getenv("MIN_SCORE", "0.0"))
    JSON_DATA_PATH = os.getenv("JSON_DATA_PATH", "data/soft_corner_rag_corpus.json")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
except Exception as e:
    raise RuntimeError(f"Failed to load config: {str(e)}")