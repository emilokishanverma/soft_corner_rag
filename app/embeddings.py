from sentence_transformers import SentenceTransformer

from app.logger import get_logger
from app.exception import ConfigurationException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)

_model = None


def get_embedding_model() -> SentenceTransformer:
    global _model

    try:
        if _model is None:
            logger.info("Loading embedding model: all-MiniLM-L6-v2")
            _model = SentenceTransformer("all-MiniLM-L6-v2")

        return _model

    except Exception as e:
        logger.exception("Failed to load embedding model")
        raise_custom_error(ConfigurationException, "Failed to load embedding model", e)


def embed_text(text: str) -> list[float]:
    try:
        if not text or not text.strip():
            raise ConfigurationException(
                "Text cannot be empty for embedding.",
                module=__name__,
                function="embed_text",
                file_name=__file__,
                line_number=0,
            )

        model = get_embedding_model()
        vector = model.encode(text).tolist()

        logger.info("Embedding generated successfully")
        return vector

    except ConfigurationException:
        raise
    except Exception as e:
        logger.exception("Failed to generate embedding")
        raise_custom_error(ConfigurationException, "Failed to generate embedding", e)