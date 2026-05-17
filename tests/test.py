import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.llm.gemini_client import generate_response


load_dotenv()

response = generate_response(
    "Explain RAG in one sentence",
    [
        {
            "content": "RAG stands for retrieval-augmented generation."
        }
    ]
)


print(response)