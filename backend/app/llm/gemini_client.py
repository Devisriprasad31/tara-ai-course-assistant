import os
import logging
from dotenv import load_dotenv

from google import genai
from google.genai import errors as genai_errors

logger = logging.getLogger(__name__)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

GEMINI_MODEL_FALLBACKS = [
    model_name.strip()
    for model_name in os.getenv(
        "GEMINI_MODEL_FALLBACKS",
        "gemini-2.5-flash-lite,gemini-2.0-flash,gemini-2.0-flash-lite"
    ).split(",")
    if model_name.strip()
]

if not GEMINI_API_KEY:
    logger.critical("GEMINI_API_KEY environment variable is not set.")
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please check your .env file.")

client = genai.Client(
    api_key=GEMINI_API_KEY
)

def build_context(retrieved_docs):
    context_parts = []
    for doc in retrieved_docs:
        context_parts.append(doc["content"])
    return "\n\n".join(context_parts)

def create_rag_prompt(query, context):
    prompt = f"""
You are an AI course assistant.

Answer the user's question ONLY using the provided context.

If there is no exact course match, recommend the closest matching courses
from the context instead of refusing. For requests about beginner AI courses,
prefer courses that are AI-related and have beginner-friendly prerequisites
such as Python or Basic Machine Learning.

If the context does not contain any relevant course information at all,
say:
"I could not find relevant course information."

Context:
{context}

Question:
{query}

Return a short, direct recommendation with 2-3 course names and a one-line
reason for each.
"""
    return prompt


def get_model_candidates():
    candidates = [GEMINI_MODEL, *GEMINI_MODEL_FALLBACKS]
    unique_candidates = []
    for model_name in candidates:
        if model_name not in unique_candidates:
            unique_candidates.append(model_name)
    return unique_candidates

def generate_response(query, retrieved_docs):
    context = build_context(retrieved_docs)
    prompt = create_rag_prompt(query, context)
    last_error = None

    for model_name in get_model_candidates():
        try:
            logger.info(f"Attempting to generate response using model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text or ""
        except genai_errors.APIError as error:
            logger.warning(f"Gemini APIError with model {model_name}: {error}")
            last_error = error
        except Exception as error:
            logger.warning(f"Unexpected error with model {model_name}: {error}")
            last_error = error

    logger.error("All Gemini model candidates failed.")
    return (
        "I could not generate a Gemini response right now. "
        f"API error: {last_error}"
    )