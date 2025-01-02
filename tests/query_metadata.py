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

