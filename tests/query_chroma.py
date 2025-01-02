import pandas as pd
from langchain_chroma import Chroma
import os
from collections import defaultdict

# Connect to ChromaDB
def connect_to_chroma(persist_directory: str, collection_name: str):
    # Initialize the Chroma database
    db = Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory
    )
    return db

# Query ChromaDB and retrieve unique document metadata
def query_chroma(db):
    # Retrieve all documents from the Chroma collection
    all_docs = db.get()
    ids = all_docs["ids"]
    metadatas = all_docs.get("metadatas", [])
    documents = all_docs.get("documents", [])

    # Aggregate results by filename
    results = defaultdict(lambda: {"word_count": 0, "metadata": None, "chunk_count": 0})
    for doc_id, metadata, content in zip(ids, metadatas, documents):
        filename = metadata.get("source", "Unknown")
        base_filename = os.path.basename(filename)
        word_count = len(content.split())

        # Aggregate word counts and track metadata
        results[base_filename]["word_count"] += word_count
        results[base_filename]["chunk_count"] += 1
        results[base_filename]["metadata"] = metadata

    return results

# Convert results to a Pandas DataFrame
def results_to_dataframe(results):
    data = []
    for filename, details in results.items():
        data.append({
            "Filename": filename,
            "Total Word Count": details["word_count"],
            "Chunk Count": details["chunk_count"],
            "Metadata": details["metadata"]
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Specify Chroma database settings
    CHROMA_DB_DIR = "./chroma_db"  # Path to your ChromaDB directory
    COLLECTION_NAME = "test_collection"  # Your collection name

    # Connect to ChromaDB
    db = connect_to_chroma(CHROMA_DB_DIR, COLLECTION_NAME)

    # Query and retrieve aggregated document details
    try:
        results = query_chroma(db)
        # Convert to DataFrame
        df = results_to_dataframe(results)

        # Display the DataFrame
        print(df)

        # Export to CSV
        output_csv = "chroma_query_results.csv"
        df.to_csv(output_csv, index=False)
        print(f"Results have been saved to {output_csv}")

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")

def inspect_metadata(db):
    all_docs = db.get()
    metadatas = all_docs.get("metadatas", [])

    unique_metadata_keys = set()
    for metadata in metadatas:
        if metadata:  # Ensure metadata is not None
            unique_metadata_keys.update(metadata.keys())

    print("Available Metadata Keys:")
    for key in unique_metadata_keys:
        print(f"- {key}")

    # Print example metadata
    if metadatas:
        print("\nExample Metadata from a Document:")
        print(metadatas[0])

if __name__ == "__main__":
    # Specify Chroma database settings
    CHROMA_DB_DIR = "./chroma_db"  # Path to your ChromaDB directory
    COLLECTION_NAME = "test_collection"  # Your collection name

    # Connect to ChromaDB
    db = connect_to_chroma(CHROMA_DB_DIR, COLLECTION_NAME)

    # Inspect metadata
    inspect_metadata(db)

