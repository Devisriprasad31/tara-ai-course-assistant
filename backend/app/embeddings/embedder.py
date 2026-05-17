from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "paraphrase-MiniLM-L3-v2"
)


def generate_embeddings(chunked_documents):

    texts = [
        chunk["content"]
        for chunk in chunked_documents
    ]

    embeddings = model.encode(texts)

    return embeddings