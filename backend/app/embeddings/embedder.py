from sentence_transformers import SentenceTransformer


_model = None


def get_model():

    global _model

    if _model is None:

        print("Loading embedding model...")

        _model = SentenceTransformer(
            "paraphrase-MiniLM-L3-v2"
        )

    return _model


def generate_embeddings(chunked_documents):

    model = get_model()

    texts = [
        chunk["content"]
        for chunk in chunked_documents
    ]

    embeddings = model.encode(texts)

    return embeddings


def generate_query_embedding(query):

    model = get_model()

    embedding = model.encode([query])

    return embedding