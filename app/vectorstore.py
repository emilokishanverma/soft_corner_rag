from qdrant_client import QdrantClient

from app.config import QDRANT_URL
from app.logger import get_logger
from app.exception import ConfigurationException, RetrieverException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)


def get_qdrant_client() -> QdrantClient:
    try:
        if not QDRANT_URL:
            raise ConfigurationException(
                "QDRANT_URL is missing.",
                module=__name__,
                function="get_qdrant_client",
                file_name=__file__,
                line_number=0,
            )

        logger.info("Connecting to Qdrant at %s", QDRANT_URL)
        return QdrantClient(url=QDRANT_URL)

    except ConfigurationException:
        raise
    except Exception as e:
        logger.exception("Failed to initialize Qdrant client")
        raise_custom_error(RetrieverException, "Failed to initialize Qdrant client", e)