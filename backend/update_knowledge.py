import argparse
import os

from app.ingestion.loader import load_courses
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.normalizer import normalize_courses, normalize_pdf_text
from app.chunking.chunker import chunk_documents
from app.embeddings.embedder import generate_embeddings
from app.retrieval.vector_store import append_to_vector_store

INDEX_PATH = "vector_store/course_index.faiss"
CHUNKS_PATH = "vector_store/chunks.pkl"

def main():
    parser = argparse.ArgumentParser(description="Update Knowledge Base")
    parser.add_argument("--json", type=str, help="Path to new JSON courses file")
    parser.add_argument("--pdf", type=str, help="Path to new PDF document")

    args = parser.parse_args()

    if not args.json and not args.pdf:
        print("Please provide either --json or --pdf path to update the knowledge base.")
        return

    documents = []

    if args.json:
        if not os.path.exists(args.json):
            print(f"Error: {args.json} does not exist.")
            return
        print(f"Loading JSON data from {args.json}...")
        raw_courses = load_courses(args.json)
        documents.extend(normalize_courses(raw_courses))

    if args.pdf:
        if not os.path.exists(args.pdf):
            print(f"Error: {args.pdf} does not exist.")
            return
        print(f"Loading PDF data from {args.pdf}...")
        raw_text = load_pdf(args.pdf)
        documents.extend(normalize_pdf_text(raw_text, source=os.path.basename(args.pdf)))

    if not documents:
        print("No documents found to process.")
        return

    print(f"Chunking {len(documents)} documents...")
    chunked_documents = chunk_documents(documents)

    print(f"Generating embeddings for {len(chunked_documents)} chunks...")
    embeddings = generate_embeddings(chunked_documents)

    print("Appending to vector store...")
    total_chunks = append_to_vector_store(INDEX_PATH, CHUNKS_PATH, embeddings, chunked_documents)

    print(f"Success! Vector store updated. New total chunks: {total_chunks}")
    print("Please restart your FastAPI server for the changes to take effect.")


if __name__ == "__main__":
    main()
