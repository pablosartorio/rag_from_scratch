# RAG from Scratch

This repository documents our journey of learning how to build a Retrieval-Augmented Generation (RAG) system from scratch. By stripping away the complexities of previous implementations (e.g., using Docker and Hugging Face's Text Generation Inference), we aim to gain a deeper understanding of RAG pipelines and their components. This project is both a practical exercise and a learning resource.

## Objective
The primary goal is to learn the fundamentals of creating a RAG system without relying on pre-configured setups. This includes:
- Setting up a custom database for document retrieval.
- Generating embeddings for textual data.
- Using LLMs (Large Language Models) for generating meaningful responses augmented by retrieved context.
- Simplifying the overall RAG system architecture.

## Overview of Progress
So far, we have:
- **Decomposed complex RAG setups**: Removed unnecessary abstractions and Docker dependencies to work directly with the core components of RAG.
- **Integrated ChromaDB**: Configured a vector database for document storage and retrieval.
- **Tested CUDA**: Ensured compatibility with NVIDIA GPUs to leverage hardware acceleration.

## Repository Structure
### Project Files
| File/Directory    | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `chroma_db/`      | Directory containing the persistent Chroma database for vector embeddings. |
| `docs/`           | Placeholder directory for additional documentation or input files.         |
| `informes/`       | Reports and detailed documentation (see below).                           |
| `LICENSE`         | Licensing information for the repository.                                  |
| `loadoc.py`       | Script to load documents into the ChromaDB database.                      |
| `testchroma.py`   | Script to test the functionality of ChromaDB.                             |
| `testcuda.py`     | Script to verify CUDA compatibility for GPU acceleration.                 |

### Informes Directory
Contains in-depth documentation and learnings:
- `Glosario.md`: Glossary of terms and concepts used throughout the project.
- `LLMs_in_GenAI.md`: Summary of the role of LLMs in generative AI workflows.
- `rag_from_scratch.md`: Overview of the project methodology.
- `RAG_Learnings.md`: Key takeaways and insights gained during the project.
- `RAG_resumen_mejoras.md`: Summary of improvements and refinements made to the system.
- `RAG_Sin_Docker.md`: Explanation of the system setup without Docker.
- `RAG_VideoChat.md`: Notes on implementing a video chat integration with RAG pipelines.

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

## Future Work
- Integrate fine-tuned LLMs for enhanced response generation.
- Explore advanced retrieval strategies for better document relevance.
- Document and test integration with Mendieta's SLURM queue for large-scale experiments.

## Contributions
This repository is developed solely by Pablo Sartorio as part of a learning project. Contributions are welcome, but please note that this is primarily a personal exploration.

## License
This project is licensed under the GNU General Public License, Version 3, 29 June 2007. See the `LICENSE` file for details.
