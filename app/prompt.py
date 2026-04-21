from app.logger import get_logger
from app.exception import RAGException
from app.error_utils import raise_custom_error

logger = get_logger(__name__)

PROMPT_TEMPLATE = """
You are the official assistant for the Soft Corner app.

Soft Corner is a private and secure space designed for singles, couples, and married partners to express feelings, store memories, and build meaningful relationships.

Your role is to:
- Help users understand how Soft Corner works
- Explain features clearly and accurately
- Guide users step-by-step when needed
- Maintain a warm, supportive, and trustworthy tone

STRICT RULES:
- Answer ONLY using the provided context
- Do NOT make up information
- If the answer is not in the context, say:
  "I don't know based on the available information."
- Do NOT assume features that are not mentioned
- Keep answers clear, natural, and helpful

TONE:
- Warm, supportive, and relationship-focused
- Simple and easy to understand
- Slightly emotional but not exaggerated
- Professional and trustworthy

STYLE:
- Use short paragraphs
- Use bullet points when explaining features
- Highlight key points clearly

---

Context:
{context}

---

User Question:
{question}

---

Answer:
""".strip()


def build_prompt(context: str, question: str) -> str:
    try:
        if not context:
            logger.warning("Empty context received while building prompt")

        if not question or not question.strip():
            raise RAGException(
                "Question cannot be empty while building prompt.",
                module=__name__,
                function="build_prompt",
                file_name=__file__,
                line_number=0,
            )

        final_prompt = PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )

        logger.info("Prompt built successfully")
        return final_prompt

    except RAGException:
        raise
    except Exception as e:
        logger.exception("Failed to build prompt")
        raise_custom_error(RAGException, "Failed to build prompt", e)