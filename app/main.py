from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.rag_chain import run_rag
from app.ingestion import ingest_documents
from app.logger import get_logger
from app.exception import AppException

logger = get_logger(__name__)

app = FastAPI(title="Soft Corner RAG API")


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    try:
        return {"message": "Soft Corner RAG API is running"}
    except Exception as e:
        logger.exception("Home endpoint failed")
        return JSONResponse(
            status_code=500,
            content={"error_code": "UNKNOWN_ERROR", "message": str(e)}
        )


@app.post("/ingest")
def ingest():
    try:
        message = ingest_documents()
        return {"message": message}

    except AppException as e:
        logger.exception("Handled application error in /ingest")
        return JSONResponse(status_code=500, content=e.to_dict())

    except Exception as e:
        logger.exception("Unexpected error in /ingest")
        return JSONResponse(
            status_code=500,
            content={"error_code": "UNKNOWN_ERROR", "message": str(e)}
        )


@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        answer = run_rag(request.question)
        return {"answer": answer}

    except AppException as e:
        logger.exception("Handled application error in /ask")
        return JSONResponse(status_code=500, content=e.to_dict())

    except Exception as e:
        logger.exception("Unexpected error in /ask")
        return JSONResponse(
            status_code=500,
            content={"error_code": "UNKNOWN_ERROR", "message": str(e)}
        )
@app.get("/health")
def health_check():
    return {"status":"running"}