from typing import List, Dict, Any

from app.config import QDRANT_COLLECTION, TOP_K, MIN_SCORE
from app.embeddings import get_embedding_model
from app.vectorstore import get_qdrant_client
from app.logger import get_logger
from app.exception  import RetrieverException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)


def extract_text_from_payload(payload: Dict[str, Any]) -> str:
    try:
        if not payload:
            return ""

        for key in ("page_content", "text", "content", "chunk_text"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        return ""

    except Exception as e:
        logger.exception("Failed to extract text from payload")
        raise_custom_error(RetrieverException, "Failed to extract text from payload", e)


def retrieve_context(
    query: str,
    qdrant_client,
    embedding_model,
    collection_name: str,
    top_k: int = TOP_K,
    min_score: float = MIN_SCORE,
) -> List[Dict[str, Any]]:
    try:
        if not query or not query.strip():
            raise RetrieverException(
                "Query cannot be empty.",
                module=__name__,
                function="retrieve_context",
                file_name=__file__,
                line_number=0,
            )

        query_vector = embedding_model.embed_query(query)

        response = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        retrieved_docs: List[Dict[str, Any]] = []

        for point in response.points:
            payload = point.payload or {}
            text = extract_text_from_payload(payload)
            score = getattr(point, "score", None)

            if not text:
                continue

            if score is not None and score < min_score:
                continue

            retrieved_docs.append(
                {
                    "id": getattr(point, "id", None),
                    "score": score,
                    "text": text,
                    "payload": payload,
                }
            )

        logger.info("Retrieved %d relevant documents", len(retrieved_docs))
        return retrieved_docs

    except RetrieverException:
        raise
    except Exception as e:
        logger.exception("Failed to retrieve documents from Qdrant")
        raise_custom_error(RetrieverException, "Failed to retrieve documents from Qdrant", e)


def build_context(docs: List[Dict[str, Any]]) -> str:
    try:
        chunks = []

        for i, doc in enumerate(docs, start=1):
            source = (
                doc["payload"].get("source")
                or doc["payload"].get("file_name")
                or doc["payload"].get("document_name")
                or "unknown_source"
            )

            chunks.append(
                f"[Document {i}]"
                f"\nSource: {source}"
                f"\nScore: {doc['score']}"
                f"\nContent:\n{doc['text']}"
            )

        return "\n\n".join(chunks)

    except Exception as e:
        logger.exception("Failed to build context")
        raise_custom_error(RetrieverException, "Failed to build context", e)


def get_runtime_dependencies():
    try:
        embedding_model = get_embedding_model()
        qdrant_client = get_qdrant_client()
        return embedding_model, qdrant_client

    except Exception as e:
        logger.exception("Failed to load runtime dependencies")
        raise_custom_error(RetrieverException, "Failed to load runtime dependencies", e)