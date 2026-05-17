import numpy as np

from app.embeddings.embedder import model


def _normalize_text(value):
    return (value or "").strip().lower()


def _score_candidate(query_text, chunk, distance):
    metadata = chunk.get("metadata", {})
    content = _normalize_text(chunk.get("content", ""))
    title = _normalize_text(metadata.get("title", ""))
    category = _normalize_text(metadata.get("category", ""))
    level = _normalize_text(metadata.get("level", ""))

    score = -float(distance)

    query_has_beginner = "beginner" in query_text or "intro" in query_text
    query_has_ai = any(
        keyword in query_text
        for keyword in ("ai", "genai", "llm", "rag", "nlp", "machine learning")
    )
    query_has_python = "python" in query_text

    if query_has_beginner and level == "beginner":
        score += 2.0
    elif query_has_beginner and level == "intermediate":
        score += 0.6

    if query_has_ai and any(
        keyword in category or keyword in title or keyword in content
        for keyword in ("artificial intelligence", "ai", "genai", "llm", "rag", "nlp")
    ):
        score += 1.5

    if query_has_python and (
        "python" in content
        or "python" in title
        or "python" in _normalize_text(
            ", ".join(metadata.get("prerequisites", []))
        )
    ):
        score += 0.75

    if query_has_beginner and query_has_ai and level != "beginner":
        if any(
            prereq in _normalize_text(", ".join(metadata.get("prerequisites", [])))
            for prereq in ("python", "basic machine learning", "generative ai basics")
        ):
            score += 0.75

    return score

def embed_query(query):

    embedding = model.encode([query])

    return np.array(
        embedding
    ).astype("float32")

def retrieve_documents(
    query,
    index,
    chunks,
    top_k=3
):

    query_embedding = embed_query(query)

    candidate_count = min(len(chunks), max(top_k, 10))

    distances, indices = index.search(
        query_embedding,
        candidate_count
    )

    query_text = _normalize_text(query)
    scored_candidates = []

    for position, idx in enumerate(indices[0]):

        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx]
        distance = distances[0][position]

        scored_candidates.append(
            (
                _score_candidate(query_text, chunk, distance),
                chunk
            )
        )

    scored_candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    retrieved_docs = [
        chunk
        for _, chunk in scored_candidates[:top_k]
    ]

    return retrieved_docs

