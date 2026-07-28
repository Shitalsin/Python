import numpy as np
import faiss

embeddings = np.load("data/embeddings.npy")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Total vectors in index:", index.ntotal)

faiss.write_index(index, "data/faiss_index.bin")

print("FAISS index saved to data/faiss_index.bin")