from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.prompt import build_prompt
from app.logger import get_logger
from app.exception import ConfigurationException, LLMException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)


def get_llm() -> Groq:
    try:
        if not GROQ_API_KEY:
            raise ConfigurationException(
                "Missing GROQ_API_KEY in environment variables.",
                module=__name__,
                function="get_llm",
                file_name=__file__,
                line_number=0,
            )

        return Groq(api_key=GROQ_API_KEY)

    except ConfigurationException:
        raise
    except Exception as e:
        logger.exception("Failed to initialize Groq client")
        raise_custom_error(LLMException, "Failed to initialize Groq client", e)


def generate_answer(context: str, question: str) -> str:
    try:
        client = get_llm()

        final_prompt = build_prompt(context, question)

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        logger.info("Groq response generated successfully")
        return answer

    except ConfigurationException:
        raise
    except Exception as e:
        logger.exception("Failed to generate answer from Groq")
        raise_custom_error(LLMException, "Failed to generate answer from Groq", e)