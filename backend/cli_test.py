# from app.ingestion.loader import load_courses
# from app.ingestion.normalizer import normalize_courses
# from app.chunking.chunker import chunk_documents

# from app.embeddings.embedder import (
#     generate_embeddings
# )

# from app.retrieval.vector_store import (
#     create_faiss_index,
#     save_index,
#     save_chunks
# )


# raw_courses = load_courses(
#     "data/courses.json"
# )

# documents = normalize_courses(
#     raw_courses
# )

# chunked_documents = chunk_documents(
#     documents
# )

# embeddings = generate_embeddings(
#     chunked_documents
# )

# index = create_faiss_index(
#     embeddings
# )

# save_index(
#     index,
#     "vector_store/course_index.faiss"
# )

# save_chunks(
#     chunked_documents,
#     "vector_store/chunks.pkl"
# )

# print("Vector store created successfully")


#after vector store cration

from app.retrieval.vector_store import (
    load_index,
    load_chunks
)

from app.retrieval.retriever import (
    retrieve_documents
)

from app.llm.gemini_client import (
    generate_response
)


index = load_index(
    "vector_store/course_index.faiss"
)

chunks = load_chunks(
    "vector_store/chunks.pkl"
)


# query = "Recommend beginner AI courses for Python developers"
query=input("Ask Tara about the courses in this platform:\n")

retrieved_docs = retrieve_documents(
    query,
    index,
    chunks
)


response = generate_response(
    query,
    retrieved_docs
)


print(response)