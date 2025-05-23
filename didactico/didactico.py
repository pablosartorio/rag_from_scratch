import string
import math

def chunk_text(text, max_length=500, overlap=50):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + max_length
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_length - overlap

    return chunks

def simple_tokenizer(text):
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    tokens = text.lower().split()
    return tokens

def build_vocabulary(chunks):
    vocab = {}
    index = 0
    for chunk in chunks:
        tokens = simple_tokenizer(chunk)
        for token in tokens:
            if token not in vocab:
                vocab[token] = index
                index += 1
    return vocab

def text_to_vector(text, vocab):
    tokens = simple_tokenizer(text)
    vector = [0] * len(vocab)
    for token in tokens:
        if token in vocab:
            index = vocab[token]
            vector[index] += 1
    return vector

def embed_text(text, vocab):
    return text_to_vector(text, vocab)

def cosine_similarity(vec1, vec2):
    dot_product = sum(a*b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a*a for a in vec1))
    magnitude2 = math.sqrt(sum(b*b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

def search(query, embeddings, chunks, vocab, top_k=5):
    query_vec = embed_text(query, vocab)
    similarities = []
    for idx, embedding in enumerate(embeddings):
        sim = cosine_similarity(query_vec, embedding)
        similarities.append((sim, idx))
    similarities.sort(reverse=True)
    top_results = similarities[:top_k]
    results = [chunks[idx] for _, idx in top_results]
    return results

# --- Modificaciones Aquí ---

# Leer el texto desde un archivo externo
with open('externo.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Paso 1: Cortar el texto
chunks = chunk_text(text)

# Paso 2: Construir el vocabulario
vocab = build_vocabulary(chunks)

# Paso 3: Generar embeddings para cada fragmento
embeddings = [embed_text(chunk, vocab) for chunk in chunks]

# Solicitar el query de búsqueda al usuario
query = input("Introduce tu pregunta: ")

# Paso 4: Buscar y recuperar fragmentos relevantes
retrieved_chunks = search(query, embeddings, chunks, vocab, top_k=5)

# Mostrar los resultados
print("\nResultados más relevantes:\n")
for i, chunk in enumerate(retrieved_chunks):
    print(f"Resultado {i+1}:\n{chunk}\n")
