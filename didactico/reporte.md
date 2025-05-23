# Reporte de los Scripts Didácticos de RAG

Este documento describe el propósito y funcionamiento de dos scripts diseñados con un enfoque didáctico para ilustrar el proceso de **Retrieval-Augmented Generation (RAG)**. Debe colocarse junto con los archivos `retrieval_test.py` y `didactico.py` en la misma carpeta para recordar fácilmente su objetivo y estructura.

---

## 1. `retrieval_test.py`

Este script aprovecha la librería **LangChain** y un almacén de vectores local (**ChromaDB**) para demostrar un flujo básico de RAG:

1. **Carga de documentos**

   * Utiliza `TextLoader` para leer un archivo de texto (por ejemplo, `inputs/tolstoy.txt`).
   * Resultado: una lista de instancias `Document` con el contenido completo.

2. **Segmentación en fragmentos (chunks)**

   * `CharacterTextSplitter` divide el texto en trozos de hasta 1000 caracteres, con 50 caracteres de solapamiento.
   * Propósito: asegurar que cada fragmento sea de tamaño manejable para el modelo de embeddings y mantener contexto entre fragmentos.

3. **Generación de embeddings**

   * Emplea `HuggingFaceEmbeddings` (modelo `all-MiniLM-L6-v2`) para convertir cada chunk en un vector de características.
   * Muestra un ejemplo imprimiendo las primeras 10 dimensiones de un embedding.

4. **Creación del almacén de vectores**

   * `Chroma.from_documents` almacena todos los embeddings en una base de datos local (`ChromaDB`).

5. **Prueba de recuperación**

   * Con la función `similarity_search`, se consulta el almacén con una pregunta (por ejemplo, "Explain war and peace") y se obtienen los 3 fragmentos más relevantes.
   * Imprime los resultados para verificar la recuperación correcta.

> **Nota:** Este flujo simula la etapa de *retrieval* en un sistema RAG, donde se obtiene información relevante antes de generar una respuesta con un LLM.

---

## 2. `didactico.py`

Este script implementa desde cero un mini-prototipo de RAG puro en Python, sin depender de librerías externas para embeddings o bases de datos de vectores:

1. **Fragmentación de texto** (`chunk_text`)

   * Divide un texto arbitrario (leído de `externo.txt`) en bloques de longitud máxima (`max_length=500`) con solapamiento (`overlap=50`).

2. **Tokenización simple** (`simple_tokenizer`)

   * Elimina puntuación, convierte a minúsculas y separa por espacios.

3. **Construcción de vocabulario** (`build_vocabulary`)

   * Recorre todos los chunks y asigna un índice único a cada palabra (token) encontrada.

4. **Representación vectorial** (`text_to_vector` / `embed_text`)

   * Para un texto dado, construye un vector de conteo de palabras basado en el vocabulario.

5. **Cálculo de similitud** (`cosine_similarity`)

   * Define la similitud coseno entre dos vectores de conteo para medir relevancia.

6. **Búsqueda y recuperación** (`search`)

   * Dado un *query*, se convierte en vector y se comparara con los embeddings de los chunks.
   * Devuelve los `top_k` fragmentos más similares.

7. **Flujo de ejecución interactivo**

   * Lee el contenido de `externo.txt`.
   * Genera chunks, vocabulario y embeddings.
   * Solicita al usuario una pregunta por `input()`.
   * Muestra los 5 resultados más relevantes en pantalla.

> **Nota:** Este script ilustra de manera clara y accesible cómo funciona internamente un esquema RAG, desde la tokenización y vectores de conteo hasta la recuperación basada en similitud.

---

## 3. Objetivo General y Próximos Pasos

* **Acercamiento didáctico a RAG:**

  * Comparar un flujo profesional (LangChain + ChromaDB) vs. una implementación casera paso a paso.
  * Entender las etapas clave: carga, segmentación, embeddings, almacenamiento y búsqueda.

* **Posibles mejoras:**

  * Integrar un LLM para generar respuestas a partir de los fragmentos recuperados (etapa *generation*).
  * Experimentar con diferentes modelos de embeddings o tamaños de chunk.
  * Persistir el vector store y ofrecer una interfaz web o API para consultas.

---
