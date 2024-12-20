from langchain_chroma import Chroma

def test_db():
    db = Chroma(collection_name="test_collection", persist_directory="./chroma_db")
    query = "Test query for retrieval"
    results = db.similarity_search(query)
    for res in results:
        print(res)

test_db()
