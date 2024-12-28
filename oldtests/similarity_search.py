from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Initialize the embeddings model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2", 
    model_kwargs={"device": "cpu"}
)

# Load the Chroma database
db = Chroma(
    collection_name="test_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Define the query
query = "visita área satelital"

# Embed the query
query_embedding = embeddings.embed_query(query)

# Perform similarity search
results = db.similarity_search_by_vector(query_embedding, k=5)  # Retrieve top 5 similar chunks

# Display results
for idx, result in enumerate(results):
    print(f"Result {idx + 1}:\n")
    print(f"Content: {result.page_content}")
    print(f"Metadata: {result.metadata}")
    print("-" * 50)

