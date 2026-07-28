import os
from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_groq import ChatGroq
from generate_answer import ask_patchcontext

load_dotenv()

test_questions = [
    "Why does FastAPI use dependency injection?",
    "Why was async support added to FastAPI routes?",
    "How does FastAPI handle path parameter type conversion?"
]

questions_list = []
answers_list = []
contexts_list = []

for q in test_questions:
    answer, cited_sources, is_safe, warnings = ask_patchcontext(q)

    context_texts = [source["text_snippet"] for source in cited_sources]
    if not context_texts:
        context_texts = ["No context retrieved."]

    questions_list.append(q)
    answers_list.append(answer)
    contexts_list.append(context_texts)

eval_data = Dataset.from_dict({
    "question": questions_list,
    "answer": answers_list,
    "contexts": contexts_list
})

judge_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

results = evaluate(
    eval_data,
    metrics=[faithfulness, answer_relevancy],
    llm=judge_llm
)

print(results)

results_df = results.to_pandas()
results_df.to_csv("data/ragas_results.csv", index=False)
print("Saved to data/ragas_results.csv")