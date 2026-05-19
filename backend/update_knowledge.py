import argparse
import os

from app.ingestion.loader import load_courses
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.normalizer import normalize_courses, normalize_pdf_text
from app.chunking.chunker import chunk_documents
from app.embeddings.embedder import generate_embeddings
from app.retrieval.vector_store import (
    append_to_vector_store,
    create_faiss_index,
    save_index,
    save_chunks
)

INDEX_PATH = "vector_store/course_index.faiss"
CHUNKS_PATH = "vector_store/chunks.pkl"

def main():
    parser = argparse.ArgumentParser(description="Update Knowledge Base")
    parser.add_argument("--json", type=str, help="Path to new JSON courses file")
    parser.add_argument("--pdf", type=str, help="Path to new PDF document")
    parser.add_argument("--md", type=str, help="Path to new Markdown document")
    parser.add_argument("--reset", action="store_true", help="Reset the knowledge base completely instead of appending")

    args = parser.parse_args()

    if not args.json and not args.pdf and not args.md:
        print("Please provide --json, --pdf, or --md path to update the knowledge base.")
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

    if args.md:
        if not os.path.exists(args.md):
            print(f"Error: {args.md} does not exist.")
            return
        print(f"Loading Markdown data from {args.md}...")
        with open(args.md, "r", encoding="utf-8") as f:
            raw_text = f.read()
        documents.extend(normalize_pdf_text(raw_text, source=os.path.basename(args.md)))

    if not documents:
        print("No documents found to process.")
        return

    print(f"Chunking {len(documents)} documents...")
    chunked_documents = chunk_documents(documents)

    print(f"Generating embeddings for {len(chunked_documents)} chunks...")
    embeddings = generate_embeddings(chunked_documents)

    print("Updating vector store...")
    if args.reset or not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        print("Creating a fresh vector store...")
        index = create_faiss_index(embeddings)
        save_index(index, INDEX_PATH)
        save_chunks(chunked_documents, CHUNKS_PATH)
        total_chunks = len(chunked_documents)
    else:
        print("Appending to vector store...")
        total_chunks = append_to_vector_store(INDEX_PATH, CHUNKS_PATH, embeddings, chunked_documents)

    print(f"Success! Vector store updated. New total chunks: {total_chunks}")
    print("Please restart your FastAPI server for the changes to take effect.")


if __name__ == "__main__":
    main()
