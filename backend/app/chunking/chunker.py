def chunk_documents(
    documents,
    chunk_size=500,
    overlap=100
):

    chunked_documents = []

    for document in documents:

        content = document["content"]
        metadata = document["metadata"]

        for i in range(0, len(content), chunk_size - overlap):

            chunk_text = content[i:i + chunk_size]

            chunk = {
                "content": chunk_text,
                "metadata": metadata
            }

            chunked_documents.append(chunk)

    return chunked_documents