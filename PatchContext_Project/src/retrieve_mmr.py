import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

with open("data/final_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

all_embeddings = np.load("data/embeddings.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")
query = "Why does FastAPI use dependency injection?"
query_embedding = model.encode([query])[0]

initial_k = 20
index = faiss.read_index("data/faiss_index.bin")
distances, indices = index.search(np.array([query_embedding]), initial_k)
candidate_indices = indices[0]

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

final_k = 5
lambda_param = 0.7

selected = []
remaining = list(candidate_indices)

while len(selected) < final_k and remaining:
    best_score = -999
    best_idx = None

    for idx in remaining:
        relevance = cosine_sim(query_embedding, all_embeddings[idx])

        if selected:
            diversity_scores = [cosine_sim(all_embeddings[idx], all_embeddings[s]) for s in selected]
            max_similarity_to_selected = max(diversity_scores)
        else:
            max_similarity_to_selected = 0

        mmr_score = lambda_param * relevance -(1 - lambda_param) *max_similarity_to_selected

        if mmr_score > best_score:
            best_score = mmr_score
            best_idx = idx

    selected.append(best_idx)
    remaining.remove(best_idx)

print("MMR-selected results for query:", query)
print()

for rank, idx in enumerate(selected):
    item = dataset[idx]
    print(f"Rank {rank+1}")
    print("Type:", item["type"])
    print("Text preview:", item["text"][:150])
    print("URL:", item["url"])
    print("---")