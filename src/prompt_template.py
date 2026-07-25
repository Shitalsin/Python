def build_prompt(query, retrieved_items):
    context_blocks = []

    for i, item in enumerate(retrieved_items):
        block = f"[Source {i+1}] (Type: {item['type']}, URL: {item['url']})\n{item['text'][:500]}"
        context_blocks.append(block)

    context_text = "\n\n".join(context_blocks)

    prompt = f"""You are PatchContext, an assistant that explains WHY design decisions were made in the FastAPI codebase, using real commits, pull requests, and issues as evidence.

Use ONLY the context below to answer the question. If the answer is not found in the context, say "I could not find enough information in the available commits, PRs, or issues to answer this confidently."

Always cite your sources using [Source X] notation when you use information from them.

Context:
{context_text}

Question: {query}

Answer:"""

    return prompt

if __name__ == "__main__":
    sample_items = [
        {"type": "issue", "url": "https://example.com/1", "text": "This is a sample issue about dependency injection."}
    ]
    test_prompt = build_prompt("Why use dependency injection?", sample_items)
    print(test_prompt)