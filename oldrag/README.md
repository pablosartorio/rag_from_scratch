# Indu Bot

Proyecto Indu-bot.

## 1. Estructura de carpetas


## 2. Iniciar un Servidor de Base de Datos Vectorial Chroma

chroma run --host 0.0.0.0 --path /db_path  

Este comando iniciara un servicio chromadb en el puerto 8000.





### **Report: How FastAPI, Chroma, LLM, LangChain, and Other Components Work Together in RAG**

---

### **1. Overview**
The system you’ve built is a **Retrieval-Augmented Generation (RAG)** pipeline. It integrates several tools and services to process user queries, retrieve relevant information, and generate contextually enriched answers using a Large Language Model (LLM).

---

### **2. Key Components**
Below is an explanation of the main components and how they interact:

#### **2.1 FastAPI**
- **Type**: **Service**
- **Role**: Acts as the API interface for user interaction.
- **Functionality**:
  - Receives user queries via HTTP GET requests.
  - Coordinates with the other components (Chroma and LLM) to process and respond to queries.

#### **2.2 Chroma**
- **Type**: **Service**
- **Role**: Acts as the vector database for document retrieval.
- **Functionality**:
  - Stores embeddings of documents for efficient similarity searches.
  - Processes search queries to retrieve the most relevant documents based on their semantic similarity to the query.

#### **2.3 LLM (Ollama)**
- **Type**: **Service**
- **Role**: Generates responses based on the user query and retrieved context.
- **Functionality**:
  - Accepts prompts from FastAPI containing user queries and contextual information from Chroma.
  - Produces natural language responses incrementally as streaming data.

#### **2.4 LangChain**
- **Type**: **Library**
- **Role**: Orchestrates and simplifies interactions with Chroma and the LLM.
- **Functionality**:
  - Handles embeddings creation using pre-trained SentenceTransformer models.
  - Manages retrieval logic and integrates context generation for the LLM prompts.

#### **2.5 Prompt Templates**
- **Type**: **Static Templates**
- **Role**: Define the structure of the input prompts sent to the LLM.
- **Functionality**:
  - Ensure that the LLM receives consistent, structured input.
  - Customize LLM behavior by providing instructions and contextual details.

---

### **3. Information Workflow**

Here’s how the components work together to process a user query:

#### **Step 1: User Query**
- The user sends a query (e.g., `"What is the capital of France?"`) to the FastAPI service at `http://localhost:8001`.

#### **Step 2: Retrieve Context from Chroma**
1. FastAPI uses LangChain's retriever to encode the user query as an embedding.
2. The embedding is sent to Chroma, which searches its vector database for the most semantically relevant documents.
3. Chroma returns the top documents (e.g., 3 most similar) as the "context."

#### **Step 3: Prepare the Prompt**
1. FastAPI formats the user query and retrieved context into a structured prompt using the pre-defined **prompt template**.
2. Example prompt:
   ```
   [INST] <<SYS>>
   Eres un historiador. Utiliza las piezas de contexto proporcionadas para responder la pregunta del usuario. 
   Si no encuentras la respuesta,en el contexto simplemente di que no la sabes, no intentes inventar una respuesta.
   Contesta de manera resumida.

   Contexto:
   France is a country in Europe. Its capital is Paris.

   Responde en idioma español.
   <</SYS>>
   What is the capital of France?[/INST]
   ```

#### **Step 4: Query the LLM**
1. FastAPI sends the formatted prompt to the LLM (Ollama) via its API at `http://127.0.0.1:11434/api/generate`.
2. The LLM processes the prompt and generates a response incrementally (streaming).

#### **Step 5: Return the Response**
1. FastAPI aggregates the streamed response from the LLM.
2. The final answer is returned to the user as plain text (e.g., `"La capital de Francia es París."`).

---

### **4. Example Information Flow**

#### **Query**: `"What is the capital of France?"`

1. **FastAPI** receives the query at the `/` endpoint.
2. **LangChain** encodes the query and sends it to **Chroma**.
   - Query: `"what is the capital of france?"` → Embedding: `[0.45, -0.12, 0.78, ...]`
3. **Chroma** searches the vector database and returns the top documents:
   - Context: `"France is a country in Europe. Its capital is Paris."`
4. **FastAPI** formats the query and context into a structured prompt using the **template**.
5. **FastAPI** sends the prompt to the **LLM** (Ollama), which generates the response incrementally:
   - `"La capital de Francia es París."`
6. **FastAPI** aggregates the response and sends it back to the user.

---

### **5. Visualization of the Workflow**

```plaintext
User Query -> FastAPI (/ endpoint) -> LangChain -> Chroma (retrieve context)
           <- Context Retrieved <-         |      
              Generate Prompt               v      
           -> FastAPI -> Ollama LLM (generate response)
                                <- Response <-       
           -> User Response <- FastAPI
```

---

### **6. Summary**
- **Services**: FastAPI (API layer), Chroma (vector database), Ollama (LLM server).
- **Libraries**: LangChain (retrieval and orchestration).
- **Static Components**: Prompt templates.
- **Flow**: Query → Retrieve → Generate → Respond.

This system efficiently combines retrieval and generation to provide contextual and accurate responses to user queries. Congratulations on getting it to work! 🎉
### **Project Improvement Report**

---

#### **Project Overview**
This report outlines the improvements made to the project, detailing the services involved, their configuration, communication flow, and exposed ports.

---

### **1. Services Overview**

| **Service**       | **Description**                                                                 | **Command to Start**           | **Port**    | **Logs**                |
|--------------------|---------------------------------------------------------------------------------|---------------------------------|-------------|-------------------------|
| **Chroma**         | Vector database used for storing and retrieving document embeddings.           | `chroma run`                   | `8000`      | `chroma.log`            |
| **RAGService**     | FastAPI service that handles queries and retrieves relevant context from Chroma.| `python RAGService.py`         | `8001`      | `rag_service.log`       |
| **GradioService**  | Web interface for user queries to interact with the RAG system.                | `python GradioService.py`      | `7000`      | `gradio_service.log`    |

---

### **2. Communication Between Services**

#### **System Workflow**
1. **Document Loading into Chroma**:
   - Documents are loaded using the `DBManagement.py` script.
   - The script preprocesses documents into chunks and stores them in a Chroma database under a specified `collection_name`.
   - This database is persisted locally for reuse across service runs.

2. **RAG Query Processing**:
   - **User Query**:
     - The user sends a query (e.g., "What is the capital of France?") to `RAGService.py` via a FastAPI endpoint (`http://127.0.0.1:8001`).
   - **Context Retrieval**:
     - `RAGService.py` retrieves relevant document chunks from the Chroma database.
     - It uses the embeddings (`all-MiniLM-L6-v2`) for matching.
   - **LLM Generation**:
     - The context and user query are passed to the LLM server for a final response.
   - **Response**:
     - The LLM server's output is returned as the response to the query.

3. **Gradio Interface**:
   - Provides a user-friendly web interface to query the system.
   - Internally, it communicates with `RAGService.py` via HTTP requests.

---

### **3. Ports Exposed**

| **Service**       | **Port** | **Purpose**                                   |
|--------------------|----------|-----------------------------------------------|
| **Chroma**         | `8000`   | Serves the vector database for document retrieval. |
| **RAGService**     | `8001`   | Processes user queries and integrates Chroma and LLM. |
| **GradioService**  | `7000`   | Hosts the Gradio web interface for user interaction. |

---

### **4. Service Communication**

#### **Internal Communication**
- **RAGService ↔ Chroma**:
  - `RAGService.py` interacts with Chroma directly via the `persist_directory` configuration or via HTTP if using the `HttpClient`.
  - Communication is local to the machine (e.g., `localhost:8000`).

- **RAGService ↔ LLM**:
  - `RAGService.py` connects to the LLM server (e.g., Ollama) via HTTP requests (`http://127.0.0.1:11434`).
  - The model used is specified in the payload (e.g., `"llama3.2"`).

#### **External Communication**
- **Gradio ↔ RAGService**:
  - Gradio queries `RAGService.py` through the HTTP API exposed on port `8001`.

---

### **5. Improvements Implemented**

1. **Chroma Database Management**:
   - Added a script (`DBManagement.py`) to load and persist documents into Chroma, ensuring the database is ready for queries.

2. **Service Logging**:
   - Logs are now saved for all services (`chroma.log`, `rag_service.log`, `gradio_service.log`) for easier debugging and monitoring.

3. **Automated Service Startup**:
   - A startup script (`start_services.sh`) was created to start all services (Chroma, RAGService, GradioService) with proper logging and sequencing.

4. **Proxy Configuration**:
   - Adjusted proxy settings for Gradio to ensure compatibility with corporate network constraints.

5. **Port Configuration**:
   - Verified and documented port usage to prevent conflicts, with options to change ports if necessary.

6. **Gradio Integration**:
   - Added a web-based Gradio interface for user-friendly query submission.

---

### **6. Example Workflow**

#### **Scenario: User Queries "What is the capital of France?"**
1. **Query Submission**:
   - The user submits the query through the Gradio interface (`http://127.0.0.1:7000`) or directly via the API (`http://127.0.0.1:8001`).

2. **Query Processing by RAGService**:
   - `RAGService.py` receives the query and retrieves relevant document chunks from Chroma (`localhost:8000`).

3. **LLM Response Generation**:
   - The query and retrieved context are sent to the LLM server (`http://127.0.0.1:11434`) for a final response.

4. **Response to User**:
   - The response (e.g., "The capital of France is Paris.") is displayed on the Gradio interface or returned as an HTTP response.

---

### **7. Current Configuration Summary**

| **Service**       | **Script/Command**         | **Port**    | **Dependencies**             |
|--------------------|----------------------------|-------------|------------------------------|
| **Chroma**         | `chroma run`              | `8000`      | Local database (`persist_directory`) |
| **RAGService**     | `python RAGService.py`    | `8001`      | Chroma, LLM server           |
| **GradioService**  | `python GradioService.py` | `7000`      | RAGService                   |

---

### **Next Steps**
- Automate the entire pipeline with system-level services (e.g., `systemctl`).
- Scale the deployment for multi-user access, with enhanced monitoring and security.
- Add support for additional document formats in `DBManagement.py`.

Let me know if you need further clarification or enhancements! 🚀
