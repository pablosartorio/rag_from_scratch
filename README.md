# RAG from Scratch

This repository documents our journey of learning how to build a Retrieval-Augmented Generation (RAG) system from scratch. By stripping away the complexities of previous implementations (e.g., using Docker and Hugging Face's Text Generation Inference), I aim to gain a deeper understanding of RAG pipelines and their components. This project is both a practical exercise and a learning resource.

## Objective
The primary goal is to learn the fundamentals of creating a RAG system without relying on pre-configured setups. This includes:
- Setting up a custom database for document retrieval. (check)
- Generating embeddings for textual data. (check)
- Using LLMs (Large Language Models) for generating meaningful(?) responses augmented by retrieved context(mejorable). (maso)
- Simplifying the overall RAG system architecture. (check)

## Overview of Progress
So far, I have:
- **Decomposed complex RAG setups**: Removed unnecessary abstractions and Docker dependencies to work directly with the core components of RAG.
- **Integrated ChromaDB**: Configured a vector database for document storage and retrieval.
- **Tested CUDA**: Ensured compatibility with NVIDIA GPUs to leverage hardware acceleration.
- **Tested Similarity Search**: tested creation of embedding with a question and search for similar chunks in the database. Also tested cosine difference. (tools used?)
- **Tested prompt creation**: including context and the info retrieved from similarity search (tools used?).
- **Tested different LLMs**: I have started with ollama (previos project) and now i have managed to try LLAMA3 via api and downloaded. I tried different things here with relative success. This is a field to explore.
- **Tested Gradio**: I started a simple gradio service and tested the access from client using ssh tunnel.
- **Integrated everything**: I have integrated all this steps in rag.py for easy reading. Next step is to separate everythin in microservices.

## Repository Structure

| File/Directory         | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `chroma_db/`           | Directory containing the persistent Chroma database for vector embeddings.  |
| `chroma_data/`         | Holds an additional Chroma SQLite database for experimentation.             |
| `docs/`                | Directory containing example and reference documents for testing.           |
| `informes/`            | Reports and detailed documentation related to the RAG project (see below).  |
| `LICENSE`              | Licensing information for the repository (GNU GPL v3).                     |
| `loadoc.py`            | Script to load documents into the ChromaDB database.                       |
| `createprompt.py`      | Script to generate prompts dynamically for testing purposes.                |
| `rag.py`               | Core script for RAG functionality and integration.                         |
| `rag_service.py`       | Backend service for connecting the RAG pipeline components.                 |
| `GradioService.py`     | Script to set up a Gradio interface for interactive RAG testing.            |
| `requirements.txt`     | File specifying Python dependencies for the project.                       |
| `test_llama3.py`       | Script to test integration with LLaMA-3 models for inference.               |
| `oldtests/`            | Deprecated test scripts for reference and historical debugging.             |
| `README.md`            | The main documentation file for the repository.                            |

---

### Informes Directory

| File                   | Description                                                                  |
|------------------------|------------------------------------------------------------------------------|
| `Glosario.md`          | Glossary of terms and concepts used throughout the project.                 |
| `llm-choose.md`        | Evaluation and comparison of LLMs for deployment (e.g., LLaMA, GPT, etc.).  |
| `LLMs_in_GenAI.md`     | Overview of the role of LLMs in generative AI workflows.                    |
| `rag_from_scratch.md`  | Detailed progress report on building the RAG system from scratch.           |
| `RAG_Learnings.md`     | Key learnings and insights gained during the RAG development process.       |
| `RAG_resumen_mejoras.md`| Summary of refinements and improvements made to the RAG system.            |
| `RAG_Sin_Docker.md`    | Explanation of the RAG system setup without Docker.                         |
| `RAG_VideoChat.md`     | Notes on implementing video chat integration with RAG pipelines.            |


## Development Environment
### Hardware
- **Server Name**: Nabucodonosor
- **OS**: Debian 6.11.10 (64-bit, kernel 6.11.10-amd64)
- **GPUs**: 3 NVIDIA GTX 1080 Ti (for local computations).
- **Cluster Access**: Mendieta Phase 2 with 24 NVIDIA A30 GPUs (via SLURM queue system).
  - [Mendieta Fase 2 Documentation](https://ccad.unc.edu.ar/equipamiento/cluster-mendieta-fase-2/)

### Software
- **Conda Environment**: The project uses a Conda environment named `rag`.
  - To recreate:
    ```bash
    conda create --name rag python=3.8
    conda activate rag
    ```
- **Python Dependencies**: Managed via `pip`. Install required packages:
  ```bash
  pip install -r requirements.txt
  ```

## Getting Started
### Steps to Run the System
1. **Set Up the Environment**:
   - Clone the repository.
   - Activate the Conda environment and install dependencies.
2. **Prepare Documents**:
   - Place documents to be indexed in the `docs/` directory.
   - Run `loadoc.py` to populate the ChromaDB database.
3. **Test Database and CUDA**:
   - Use `testchroma.py` to validate database functionality.
   - Run `testcuda.py` to ensure GPU acceleration is available.
4. **Start Development**:
   - Build and test the RAG pipeline incrementally.
5. **bash commands**:
   - python rag.py
   - ssh -L 7000:localhost:7000 nabu (from client)
   - http://localhost:7000 (from client) or curl http://localhost:7000

## Future Work
- Separate everythin in micro services and learn advanced rag techniques:
    - Database update
    - Data: translated audios, clean data, how this tipe of data impact in the whole process
    - Chunk and embedding creation
    - Similarity search, diversify and mix methods
    - Rank
    - Context
    - Prompt creation and engineer
    - Try LLMs, local, api, cloud service (Algo en INVAP - UNC Mendieta - Amazon)
    - Tests and benckmark results

## Contributions
This repository is developed by Pablo Sartorio as part of a learning project. Contributions are welcome, but please note that this is primarily a personal exploration.

## License
This project is licensed under the GNU General Public License, Version 3, 29 June 2007. See the `LICENSE` file for details.
