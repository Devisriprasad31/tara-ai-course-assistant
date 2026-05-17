import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.retrieval.vector_store import load_index, load_chunks
from app.retrieval.retriever import retrieve_documents
from app.llm.gemini_client import generate_response

# Configure standard logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AppState:
    index = None
    chunks = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load vector store on startup securely
    logger.info("Application starting up. Loading vector store...")
    try:
        AppState.index = load_index("vector_store/course_index.faiss")
        AppState.chunks = load_chunks("vector_store/chunks.pkl")
        logger.info(f"Vector store loaded successfully. Total chunks: {len(AppState.chunks)}")
    except Exception as e:
        logger.error(f"Failed to load vector store on startup: {e}")
        logger.warning("Application running without vector store initialized. Will return errors for chat requests.")
    yield
    # Clean up on shutdown
    logger.info("Application shutting down. Cleaning up resources...")
    AppState.index = None
    AppState.chunks = None

app = FastAPI(lifespan=lifespan)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Received chat request: '{request.query}'")
    if not AppState.index or not AppState.chunks:
        logger.error("Chat request failed: Vector store is not initialized.")
        return ChatResponse(response="Vector store is not initialized or missing. Please try again later.")

    try:
        # Retrieve relevant documents
        retrieved_docs = retrieve_documents(request.query, AppState.index, AppState.chunks)
        logger.info(f"Retrieved {len(retrieved_docs)} relevant documents.")

        # Generate response
        response_text = generate_response(request.query, retrieved_docs)
        logger.info("Successfully generated AI response.")

        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Failed to process chat request: {e}")
        return ChatResponse(response="An internal error occurred while processing your request.")

@app.get("/")
async def root_health_check():
    return {"status": "Backend running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
