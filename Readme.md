# 📌 Soft Corner RAG API (Qdrant + Groq)

---

## 🚀 Overview

This project is a **Retrieval-Augmented Generation (RAG) API** built using:

* **FastAPI** → API layer
* **Qdrant** → Vector database
* **SentenceTransformers (`all-MiniLM-L6-v2`)** → Text → Vector conversion
* **Groq (LLM)** → Answer generation
* **Custom Logger + Exceptions** → Production-style error handling

---

## 🧠 How It Works

### 🔄 Flow

```text
User Question
   ↓
FastAPI (/ask)
   ↓
Embedding Model (MiniLM)
   ↓
Qdrant Search (query_points)
   ↓
Relevant Documents
   ↓
Build Context
   ↓
Prompt Injection
   ↓
Groq LLM
   ↓
Final Answer
```

---

## ❗ Important Architecture Notes

* ❌ **NO LangChain Retriever used**
* ✅ **Direct Qdrant retrieval used**
* ✅ **Same embedding model used for ingestion and query**
* ✅ Lightweight embedding model: `all-MiniLM-L6-v2`
* ✅ Data source:

```bash
data/soft_corner_rag_corpus.json
```

---

## 📁 Project Structure

```bash
app/
│
├── config.py          # Environment & config loader
├── logger.py          # Logging system
├── exception.py       # Custom exception classes
├── error_utils.py     # Error context helper
├── embeddings.py      # Embedding model (MiniLM)
├── ingestion.py       # JSON → Qdrant ingestion
├── vectorstore.py     # Qdrant client
├── retriever.py       # Direct Qdrant retrieval
├── prompt.py          # Prompt template
├── llm.py             # Groq integration
├── rag_chain.py       # Main pipeline
├── main.py            # FastAPI app
│
run.py                 # App runner
.env                   # Environment variables
```

---

## ⚙️ Setup

### 1. Create Virtual Environment (Recommended)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages include:

* fastapi
* uvicorn
* python-dotenv
* groq
* qdrant-client
* sentence-transformers
* pydantic

---

### 3. Start Qdrant (Docker)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

### 4. Configure `.env`

```env
GROQ_API_KEY=your_api_key

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=soft_corner_docs

GROQ_MODEL=llama-3.3-70b-versatile

TOP_K=6
MIN_SCORE=0.0

JSON_DATA_PATH=data/soft_corner_rag_corpus.json

LOG_FILE=logs/app.log
```

---

## 📥 Data Ingestion

Place your data file here:

```bash
data/soft_corner_rag_corpus.json
```

### JSON Format

```json
[
  {
    "page_content": "Some text here",
    "metadata": {
      "source": "file1"
    }
  }
]
```

---

### ▶️ Run Local Ingestion

```bash
python local_ingest.py
```

This will:

* Read JSON
* Generate embeddings using `all-MiniLM-L6-v2`
* Store vectors in Qdrant

⚠️ **Note:**
`recreate_collection()` will delete previous data.

---

## 💬 Ask Questions

### Endpoint

```bash
POST /ask
```

### Request

```json
{
  "question": "What is Maximum Privacy?"
}
```

### Response

```json
{
  "answer": "..."
}
```

---

## 🌐 API Access

### Base URL

```bash
http://127.0.0.1:5000
```

### Health Check

```bash
http://127.0.0.1:5000/health
```

### Swagger Docs

```bash
http://127.0.0.1:5000/docs
```

---

## 🧾 Prompt Behavior

The system follows strict RAG rules:

* Answers ONLY from provided context
* No hallucination
* If not found:

  > "I don't know based on the available information."

---

## 🛠 Features

* ✅ Direct Qdrant retrieval (`query_points`)
* ✅ Lightweight embedding model
* ✅ No LangChain dependency
* ✅ Modular architecture
* ✅ Custom logging system
* ✅ Structured exception handling
* ✅ Clean separation of concerns

---

## ⚠️ Notes

* `TOP_K` controls number of retrieved documents
* `MIN_SCORE` filters weak matches
* Embedding model is loaded once and reused
* Ensure Qdrant is running before API start

---

## 🧠 Summary

* `.env` → stores config values
* `config.py` → loads config
* `SentenceTransformer` → creates embeddings
* `Qdrant` → stores vectors
* `Retriever` → fetches relevant docs
* `Groq` → generates answers

---

## 🟢 Run the Server

Make sure your `run.py` contains:

```python
uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
```

Start server:

```bash
python run.py
```

---

## 👌 Done

Your RAG API is now:

* ✅ Lightweight
* ✅ Modular
* ✅ No heavy dependencies
* ✅ Production-ready (structure-wise)
* ✅ Easy to deploy

---
