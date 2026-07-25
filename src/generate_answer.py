import json
import numpy as np
import faiss
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq
from prompt_template import build_prompt

load_dotenv()

with open("data/final_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

all_embeddings = np.load("data/embeddings.npy")
index = faiss.read_index("data/faiss_index.bin")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_mmr(query, final_k=5, initial_k=20, lambda_param=0.7):
    query_embedding = embed_model.encode([query])[0]

    distances, indices = index.search(np.array([query_embedding]), initial_k)
    candidate_indices = list(indices[0])

    selected = []
    remaining = candidate_indices

    while len(selected) < final_k and remaining:
        best_score = -999
        best_idx = None

        for idx in remaining:
            relevance = cosine_sim(query_embedding, all_embeddings[idx])

            if selected:
                max_similarity_to_selected = max(
                    cosine_sim(all_embeddings[idx], all_embeddings[s]) for s in selected)
            else:
                max_similarity_to_selected = 0

            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_similarity_to_selected

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx
        selected.append(best_idx)
        remaining.remove(best_idx)
    return [dataset[idx] for idx in selected]

def ask_patchcontext(query):
    retrieved_items = retrieve_mmr(query)

    prompt = build_prompt(query, retrieved_items)

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return answer, retrieved_items

if __name__ == "__main__":
    query = "Why does FastAPI use dependency injection?"
    answer, sources = ask_patchcontext(query)

    print("QUESTION:", query)
    print()
    print("ANSWER:")
    print(answer)
    print()
    print("SOURCES USED:")
    for i, item in enumerate(sources):
        print(f"[Source {i+1}] {item['url']}")