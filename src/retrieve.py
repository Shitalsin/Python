import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

with open("data/final_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)
index = faiss.read_index("data/faiss_index.bin")

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "Why does FastAPI use dependency injection?"

query_embedding = model.encode([query])
k = 5

distances, indices = index.search(query_embedding, k)

print("Top", k, "results for query:", query)
print()

for rank, idx in enumerate(indices[0]):
    item = dataset[idx]
    print(f"Rank {rank+1} (distance: {distances[0][rank]:.4f})")
    print("Type:", item["type"])
    print("Text preview:", item["text"][:150])
    print("URL:", item["url"])
    print("---")