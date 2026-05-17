import faiss
import numpy as np
import pickle

def create_faiss_index(embeddings):

    embedding_matrix = np.array(
        embeddings
    ).astype("float32")

    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embedding_matrix)

    return index

def save_index(index, path):

    faiss.write_index(index, path)

def load_index(path):

    return faiss.read_index(path)

def save_chunks(chunks, path):

    with open(path, "wb") as file:
        pickle.dump(chunks, file)

def load_chunks(path):

    with open(path, "rb") as file:
        return pickle.load(file)

def append_to_vector_store(index_path, chunks_path, new_embeddings, new_chunks):
    # Load existing
    index = load_index(index_path)
    chunks = load_chunks(chunks_path)

    # Append FAISS index
    embedding_matrix = np.array(new_embeddings).astype("float32")
    index.add(embedding_matrix)

    # Append chunks
    chunks.extend(new_chunks)

    # Save back
    save_index(index, index_path)
    save_chunks(chunks, chunks_path)

    return len(chunks)