from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL_NAME
from app.logger import get_logger
from app.exception import ConfigurationException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)


def get_embedding_model() -> HuggingFaceEmbeddings:
    try:
        if not EMBEDDING_MODEL_NAME:
            raise ConfigurationException(
                "EMBEDDING_MODEL_NAME is missing.",
                module=__name__,
                function="get_embedding_model",
                file_name=__file__,
                line_number=0,
            )

        logger.info("Loading embedding model: %s", EMBEDDING_MODEL_NAME)
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    except ConfigurationException:
        raise
    except Exception as e:
        logger.exception("Failed to load embedding model")
        raise_custom_error(ConfigurationException, "Failed to load embedding model", e)