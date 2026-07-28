import re       # Python built-in regex library
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

def extract_cited_sources(answer_text, retrieved_items):
    cited_numbers = re.findall(r"\[Source (\d+)\]", answer_text)
    cited_numbers = set(int(n) for n in cited_numbers)

    cited_sources = []
    for i, item in enumerate(retrieved_items):
        source_number = i + 1
        if source_number in cited_numbers:
            cited_sources.append({
                "source_number": source_number,
                "type": item["type"],
                "url": item["url"],
                "text_snippet": item["text"][:200]
            })

    return cited_sources

def check_hallucination(answer_text, retrieved_items, cited_sources):
    warnings = []

    all_source_numbers = re.findall(r"\[Source (\d+)\]", answer_text)
    all_source_numbers = set(int(n) for n in all_source_numbers)

    max_valid_number = len(retrieved_items)
    invalid_citations = [n for n in all_source_numbers if n > max_valid_number or n < 1]

    if invalid_citations:
        warnings.append(f"Answer cites source numbers that don't exist: {invalid_citations}")

    if not cited_sources:
        warnings.append("Answer contains no valid citations - claims may be ungrounded.")
    else:
        cited_text = " ".join(item["text_snippet"] for item in cited_sources)

        answer_embedding = embed_model.encode([answer_text])[0]
        cited_embedding = embed_model.encode([cited_text])[0]

        grounding_score = cosine_sim(answer_embedding, cited_embedding)

        if grounding_score < 0.3:
            warnings.append(f"Low semantic overlap between answer and cited sources (score: {grounding_score:.2f}). Answer may contain unsupported claims.")

    is_safe = len(warnings) == 0

    return is_safe, warnings

def ask_patchcontext(query):
    retrieved_items = retrieve_mmr(query)

    prompt = build_prompt(query, retrieved_items)

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    cited_sources = extract_cited_sources(answer, retrieved_items)
    is_safe, warnings = check_hallucination(answer, retrieved_items, cited_sources)
    return answer, cited_sources, is_safe, warnings

if __name__ == "__main__":
    query = "Why does FastAPI use dependency injection?"
    answer, sources, is_safe, warnings = ask_patchcontext(query)

    print("QUESTION:", query)
    print()
    print("ANSWER:")
    print(answer)
    print()
    print("CITED SOURCES:")
    for source in sources:
        print(f"[Source {source['source_number']}] ({source['type']}) {source['url']}")

    print()
    print("HALLUCINATION CHECK:")
    print("Is safe:", is_safe)
    if warnings:
        for w in warnings:
            print("⚠️", w)