from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Initialize ChromaDB connection
def initialize_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    db = Chroma(
        collection_name="test_collection",
        embedding_function=embeddings,
        persist_directory="/users/psartorio/rag_from_scratch/chroma_db"  # Ensure this matches your setup
    )
    return db, embeddings

# Retrieve relevant chunks
def retrieve_relevant_chunks(query, db, embeddings, k=3):
    query_embedding = embeddings.embed_query(query)
    results = db.similarity_search_by_vector(query_embedding, k=k)
    return results

# Generate augmented prompt
def generate_prompt(query, relevant_chunks):
    context = "\n".join(chunk.page_content for chunk in relevant_chunks)
    prompt_template = (
        "[INST] <<SYS>>\n"
        "Usa el contexto provista pra responder la pregunta del usuario."
        "Si la respuesta no puede ser encontrada en el contesto responde con \"No se, y eso también está bien.\"\n"
        "Context:\n"
        "{context}\n\n"
        "Question:\n"
        "{query}\n"
        "[/INST]"
    )
    return prompt_template.format(context=context, query=query)

# Main function
def main():
    # Initialize database and embeddings
    db, embeddings = initialize_db()

    # User input
    query = "¿Cómo preparar tortilla de papas?"  # Example query

    # Print the query
    print(f"Query: {query}\n")

    # Retrieve relevant chunks
    print("Retrieving relevant chunks...")
    relevant_chunks = retrieve_relevant_chunks(query, db, embeddings, k=3)

    print("Relevant Chunks:")
    for idx, chunk in enumerate(relevant_chunks):
        print(f"Chunk {idx + 1}: {chunk.page_content[:200]}...")  # Print first 200 characters of each chunk
    
    # Generate the prompt
    print("\nGenerating augmented prompt...")
    prompt = generate_prompt(query, relevant_chunks)
    print("Generated Prompt:\n")
    print(prompt)

if __name__ == "__main__":
    main()
