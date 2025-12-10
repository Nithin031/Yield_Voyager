import json
import numpy as np
import faiss
import ollama

# Load everything
cases = json.load(open("cases_clean.json", "r", encoding="utf-8"))
embeddings = np.load("embeddings.npy")
index = faiss.read_index("faiss.index")

# Helper: embed any new text query
def embed(text):
    out = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return np.array(out["embedding"], dtype="float32")

# Retrieval
def retrieve(query, k=3):
    q_emb = embed(query)
    q_emb = np.array([q_emb])
    faiss.normalize_L2(q_emb)

    D, I = index.search(q_emb, k)
    return [(cases[i], float(D[0][pos])) for pos, i in enumerate(I[0])]

# LLM generator
def generate_answer(query, retrieved):
    context = ""
    for case, score in retrieved:
        context += (
            f"Case: {case['case_name']}\n"
            f"Jurisdiction: {case['jurisdiction']}\n"
            f"Year: {case['year_of_judgment']}\n"
            f"Principles: {', '.join(case['key_legal_principles'])}\n"
            f"Outcome: {case['case_outcome']}\n\n"
        )

    prompt = f"""
Use only the context below to answer the question.
Do not hallucinate. Cite relevant cases when needed.

Context:
{context}

Question:
{query}

Answer:
"""

    resp = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp["message"]["content"]
