import numpy as np
from sentence_transformers import SentenceTransformer
from generate_answer import ask_patchcontext

embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def evaluate_faithfulness(answer, contexts):
    if not contexts:
        return 0.0
    combined_context = " ".join(contexts)
    answer_emb = embed_model.encode([answer])[0]
    context_emb = embed_model.encode([combined_context])[0]
    return float(cosine_sim(answer_emb, context_emb))


def evaluate_answer_relevancy(answer, question):
    answer_emb = embed_model.encode([answer])[0]
    question_emb = embed_model.encode([question])[0]
    return float(cosine_sim(answer_emb, question_emb))


test_questions = [
    "Why does FastAPI use dependency injection?",
    "Why was async support added to FastAPI routes?",
    "How does FastAPI handle path parameter type conversion?"
]

print(f"{'Question':<50} {'Faithfulness':<15} {'Relevancy':<15}")
print("-" * 80)

total_faithfulness = 0
total_relevancy = 0

for q in test_questions:
    answer, cited_sources, is_safe, warnings = ask_patchcontext(q)
    contexts = [source["text_snippet"] for source in cited_sources]

    faithfulness_score = evaluate_faithfulness(answer, contexts)
    relevancy_score = evaluate_answer_relevancy(answer, q)

    total_faithfulness += faithfulness_score
    total_relevancy += relevancy_score

    print(f"{q[:47]+'...':<50} {faithfulness_score:<15.3f} {relevancy_score:<15.3f}")

avg_faithfulness = total_faithfulness / len(test_questions)
avg_relevancy = total_relevancy / len(test_questions)

print("-" * 80)
print(f"Average Faithfulness: {avg_faithfulness:.3f}")
print(f"Average Answer Relevancy: {avg_relevancy:.3f}")