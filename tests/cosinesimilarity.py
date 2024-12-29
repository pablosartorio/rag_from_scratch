import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Example: Compute cosine similarity between query embedding and a chunk embedding
chunk_embedding = db.get_embedding(0)  # Example: Get first chunk embedding (modify as needed)
similarity = cosine_similarity(query_embedding, chunk_embedding)
print(f"Cosine Similarity: {similarity}")
