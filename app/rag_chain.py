from app.config import QDRANT_COLLECTION, TOP_K, MIN_SCORE
from app.llm import generate_answer
from app.retriever import retrieve_context, build_context, get_runtime_dependencies
from app.logger import get_logger
from app.exception import RAGException, RetrieverException, LLMException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)


def run_rag(query: str) -> str:
    try:
        if not query or not query.strip():
            raise RAGException(
                "Query cannot be empty.",
                module=__name__,
                function="run_rag",
                file_name=__file__,
                line_number=0,
            )

        logger.info("Running RAG for query: %s", query)

        qdrant_client = get_runtime_dependencies()

        docs = retrieve_context(
            query=query,
            qdrant_client=qdrant_client,
            collection_name=QDRANT_COLLECTION,
            top_k=TOP_K,
            min_score=MIN_SCORE,
        )

        if not docs:
            logger.warning("No relevant context found")
            return "I don't know based on the available information."

        context = build_context(docs)
        answer = generate_answer(context=context, question=query)

        logger.info("RAG completed successfully")
        return answer

    except (RAGException, RetrieverException, LLMException):
        raise
    except Exception as e:
        logger.exception("Failed to run RAG pipeline")
        raise_custom_error(RAGException, "Failed to run RAG pipeline", e)