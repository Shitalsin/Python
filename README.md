# PatchContext

A RAG system that answers "why" questions about FastAPI's design decisions using commits, PRs, and issues as evidence.

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `.\venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Add `.env` file with `GROQ_API_KEY` and `GITHUB_TOKEN`

## Pipeline
1. `src/collect_commits.py`, `collect_prs.py`, `collect_issues.py` — data collection
2. `src/clean_data.py` — cleaning and merging
3. `src/create_embeddings.py` — generate embeddings
4. `src/build_faiss_index.py` — build vector index
5. `src/generate_answer.py` — core RAG pipeline
6. `app.py` — Streamlit UI

## Run
`streamlit run app.py`