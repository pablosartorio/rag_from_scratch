from langchain_chroma import Chroma

try:
    db = Chroma(
        collection_name="test_collection",
        persist_directory="/users/psartorio/rag_from_scratch/chroma_db"
    )
    documents = db.get()["documents"]
    print(f"Número de documentos en la base de datos: {len(documents)}")
    for i, doc in enumerate(documents[:5]):  # Muestra los primeros 5 documentos
        print(f"\nDocumento {i+1}:\n{doc}")
except Exception as e:
    print(f"Error al acceder a la base de datos: {e}")
