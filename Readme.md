# 📌 Soft Corner RAG API (Qdrant + Groq)

## 🚀 Overview

This project is a **Retrieval-Augmented Generation (RAG) API** built using:

* **FastAPI** → API layer
* **Qdrant** → Vector database
* **HuggingFace Embeddings** → Text → Vector conversion
* **Groq (LLM)** → Answer generation
* **Custom Logger + Exceptions** → Production-style error handling

It allows you to:

* Ingest data from JSON
* Store embeddings in Qdrant
* Retrieve relevant context
* Generate grounded answers using an LLM

---

## 🧠 How It Works

### 🔄 Flow

```text
User Question
   ↓
FastAPI (/ask)
   ↓
Embedding Model
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

  ```python
  qdrant_client.query_points(...)
  ```
* ✅ Data is loaded from:

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
├── exceptions.py      # Custom exception classes
├── error_utils.py     # Error context helper
├── embeddings.py      # Embedding model loader
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

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Start Qdrant (Docker)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

### 3. Configure `.env`

```env
GROQ_API_KEY=your_api_key

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=soft_corner_docs

EMBEDDING_MODEL_NAME=BAAI/bge-small-en-v1.5

TOP_K=6
MIN_SCORE=0.0

JSON_DATA_PATH=data/soft_corner_rag_corpus.json

GROQ_MODEL=llama-3.3-70b-versatile

LOG_FILE=logs/app.log
```

---

## 📥 Data Ingestion

Place your file here:

```bash
data/soft_corner_rag_corpus.json
```

### Format:

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

### Run ingestion API

```bash
POST /ingest
```

This will:

* Read JSON
* Generate embeddings
* Store in Qdrant

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

## 🧾 Prompt Used

The system uses a strict RAG prompt:

* Only answers from context
* No hallucination
* If not found:

  > "I don't know based on the available information."

---

## 🛠 Features

* ✅ Direct Qdrant retrieval
* ✅ Custom logging system
* ✅ Structured error handling
* ✅ Modular architecture
* ✅ Config-driven system
* ✅ JSON ingestion pipeline
* ✅ Clean separation of concerns

---

## ⚠️ Notes

* `recreate_collection()` will **delete old data**
* Use carefully in production
* `TOP_K` controls number of retrieved docs
* `MIN_SCORE` filters weak matches

---

## 🔥 Future Improvements

* Add reranking
* Add source citations
* Streaming responses
* Async API
* Hybrid search (keyword + vector)

---

## 🧠 Summary

* `.env` → stores values
* `config.py` → loads values
* Qdrant → stores embeddings
* Retriever → fetches relevant docs
* Groq → generates answers

---

## 🟢 Run the Server

```bash
python run.py
```

Open:

```bash
http://127.0.0.1:8000/docs
```

---

## 👌 Done

Your RAG API is now:

* clean
* modular
* production-ready (structure-wise)
* and fully understandable

---
