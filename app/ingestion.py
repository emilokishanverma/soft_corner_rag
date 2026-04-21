import json
from typing import List

from langchain_core.documents import Document
from qdrant_client import models

from app.config import JSON_DATA_PATH, QDRANT_COLLECTION
from app.embeddings import get_embedding_model
from app.vectorstore import get_qdrant_client
from app.logger import get_logger
from app.exception import IngestionException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)


def load_documents_from_json(path: str = JSON_DATA_PATH) -> List[Document]:
    try:
        logger.info("Loading JSON data from: %s", path)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents: List[Document] = []
        for item in data:
            try:
                documents.append(
                    Document(
                        page_content=item["page_content"],
                        metadata=item.get("metadata", {})
                    )
                )
            except KeyError as e:
                logger.warning("Skipping invalid item, missing key: %s", str(e))
            except Exception as e:
                logger.warning("Skipping invalid item: %s", str(e))

        logger.info("Loaded %d documents from JSON", len(documents))
        return documents

    except FileNotFoundError as e:
        logger.exception("JSON file not found")
        raise_custom_error(IngestionException, f"JSON file not found: {path}", e)
    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON format")
        raise_custom_error(IngestionException, "Invalid JSON format", e)
    except Exception as e:
        logger.exception("Failed to load documents from JSON")
        raise_custom_error(IngestionException, "Failed to load documents from JSON", e)


def ingest_documents(path: str = JSON_DATA_PATH) -> str:
    try:
        documents = load_documents_from_json(path)

        if not documents:
            raise IngestionException(
                "No valid documents found for ingestion.",
                module=__name__,
                function="ingest_documents",
                file_name=__file__,
                line_number=0,
            )

        embedding_model = get_embedding_model()
        qdrant_client = get_qdrant_client()

        sample_vector = embedding_model.embed_query("test")
        vector_size = len(sample_vector)

        logger.info("Recreating Qdrant collection: %s", QDRANT_COLLECTION)
        qdrant_client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            ),
        )

        points = []
        for idx, doc in enumerate(documents):
            vector = embedding_model.embed_query(doc.page_content)
            payload = {
                "page_content": doc.page_content,
                **doc.metadata
            }

            points.append(
                models.PointStruct(
                    id=idx,
                    vector=vector,
                    payload=payload
                )
            )

        logger.info("Uploading %d points to Qdrant", len(points))
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=points
        )

        logger.info("Documents ingested successfully into Qdrant")
        return "Embedding + Qdrant DB created successfully."

    except IngestionException:
        raise
    except Exception as e:
        logger.exception("Failed to ingest documents into Qdrant")
        raise_custom_error(IngestionException, "Failed to ingest documents into Qdrant", e)