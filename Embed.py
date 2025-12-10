import json
import numpy as np
import faiss
import ollama

# -----------------------------------------------------------
# 1. Load your JSON file (list of case dictionaries)
# -----------------------------------------------------------
with open(r"D:\ACM TASKS\New folder\LEGAL_CASES JSON.json", "r", encoding="utf-8") as f:
    cases = json.load(f)

print("Loaded cases:", len(cases))

# -----------------------------------------------------------
# 2. Helper function to generate embeddings using Ollama
# -----------------------------------------------------------

def get_embedding(text, model="nomic-embed-text"):
    response = ollama.embeddings(model=model, prompt=text)
    return response["embedding"]


# -----------------------------------------------------------
# 3. Prepare text for each case
#    (this determines retrieval quality)
# -----------------------------------------------------------

texts = []

for case in cases:
    text = (
        f"{case['case_name']} "
        f"{case['case_type']} "
        f"{case['jurisdiction']} "
        f"{case['year_of_judgment']} "
        f"{' '.join(case['key_legal_principles'])} "
        f"{case['case_outcome']}"
    )
    texts.append(text)


# -----------------------------------------------------------
# 4. Generate embeddings for all cases
# -----------------------------------------------------------

print("Generating embeddings...")

emb_list = []
for t in texts:
    emb = get_embedding(t)
    emb_list.append(emb)

embeddings_np = np.array(emb_list).astype("float32")
print("Embedding matrix shape:", embeddings_np.shape)


# -----------------------------------------------------------
# 5. Create FAISS index (cosine similarity)
# -----------------------------------------------------------

faiss.normalize_L2(embeddings_np)

dimension = embeddings_np.shape[1]
index = faiss.IndexFlatIP(dimension)

index.add(embeddings_np)

print("FAISS index built.")
print("Total vectors indexed:", index.ntotal)


faiss.write_index(index, "faiss.index")
np.save("embeddings.npy", embeddings_np)

with open("cases_clean.json", "w", encoding="utf-8") as f:
    json.dump(cases, f, indent=2)

print("Saved: faiss.index, embeddings.npy, cases_clean.json")
