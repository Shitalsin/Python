import json
from sentence_transformers import SentenceTransformer
import numpy as np

with open("data/final_dataset.json","r",encoding="utf-8") as f:
    dataset= json.load(f)

print("Total items to embed:",len(dataset))

model=SentenceTransformer("all-MiniLM-L6-v2")

texts=[item["text"] for item in dataset]

embeddings=model.encode(texts,show_progress_bar=True)

print("Embeddings shape:",embeddings.shape)
np.save("data/embeddings.npy",embeddings)
print("Embeddings saved to data/embeddings.npy")