import os
import requests
import logging
import numpy as np
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Use exactly the same model as before for consistency
MODEL_ID = "sentence-transformers/paraphrase-MiniLM-L3-v2"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}/pipeline/feature-extraction"

headers = {}
if HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != "your_huggingface_key_here":
    headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"
else:
    logger.error("HUGGINGFACE_API_KEY is not set or invalid. Hugging Face Inference API requires authentication.")
    raise ValueError("HUGGINGFACE_API_KEY is required to generate embeddings. Please add a valid key to your .env file.")


def _call_huggingface_api(texts):
    """
    Calls the HuggingFace Inference API for the specified texts.
    Returns a numpy array of embeddings (float32).
    """
    try:
        logger.info(f"Sending {len(texts)} texts to HuggingFace Inference API...")
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": texts},
            timeout=15  # 15 seconds timeout
        )
        response.raise_for_status()
        
        # The API returns a list of lists for multiple texts
        embeddings = response.json()
        
        return np.array(embeddings).astype("float32")
    except requests.exceptions.Timeout:
        logger.error("HuggingFace Inference API request timed out.")
        raise RuntimeError("Embedding generation timed out.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HuggingFace API HTTP Error: {response.text}")
        raise RuntimeError(f"Embedding generation failed with HTTP error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error calling HuggingFace API: {e}")
        raise RuntimeError(f"Embedding generation failed: {e}")


def generate_embeddings(chunked_documents):
    """
    Generates embeddings for a batch of chunked documents.
    """
    if not chunked_documents:
        return np.array([]).astype("float32")

    texts = [chunk["content"] for chunk in chunked_documents]
    return _call_huggingface_api(texts)


def generate_query_embedding(query):
    """
    Generates an embedding for a single query.
    Returns a numpy array (1, D).
    """
    if not query:
        raise ValueError("Query cannot be empty.")
    
    embeddings = _call_huggingface_api([query])
    return embeddings