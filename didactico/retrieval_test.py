from langchain_community.document_loaders import TextLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

# Step 1: Load your documents
loader = TextLoader("inputs/tolstoy.txt")
documents = loader.load()

# Step 2: Split documents into chunks (default: 1000 characters per chunk)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Print out some of the chunks to see how the text is split
print("Sample Chunks:")
for idx, doc in enumerate(docs[10:12]):  # Adjust the number to see more chunks
    print(f"Chunk {idx+1}:\n{doc.page_content}\n")

# Step 3: Use SentenceTransformer to convert text chunks into embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# To see embeddings, you can generate them directly
sample_text = docs[11].page_content  # Let's take the first chunk
sample_embedding = embedding_model.embed_documents([sample_text])[0]

# Print only the first 10 elements of the embedding
print(f"First 10 dimensions of the embedding:\n{sample_embedding[:10]}\n")

## Step 4: Create a local ChromaDB vector store
vector_store = Chroma.from_documents(docs, embedding_model)

#
## Step 5: Test retrieval by running a sample query
query = "Explain war and peace"
results = vector_store.similarity_search(query, k=3)

# Step 6: Print the results
for idx, result in enumerate(results):
    print(f"Result {idx+1}:\n{result.page_content}\n")
