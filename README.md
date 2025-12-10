I first created a combined dataset of around 965 legal cases. Some of them were well-known landmark cases that I manually formatted, and the rest were generated synthetically in the same structure to expand the dataset. Each case includes fields such as case name, jurisdiction, year, legal principles, parties, and outcome.

Every case was converted into a single text chunk so an embedding model could process it. I used the nomic-embed-text model from Ollama to generate 768-dimensional embeddings for all cases. These embeddings represent the semantic meaning of each case and allow similarity-based retrieval instead of just keyword matching.

After generating embeddings, I normalized them and stored all vectors inside a FAISS index. This index makes it possible to perform fast vector searches. A user query is embedded the same way and passed to FAISS, which returns the top-k most relevant cases.

For the generation step, the retrieved case summaries are given to an LLM (Llama 3) to produce an answer grounded only in the provided context. This forms the “G” in the RAG pipeline. The last step is a simple UI that accepts a question, shows the retrieved chunks, and displays the LLM’s final answer.

Overall, the project demonstrates the full flow of a RAG system: dataset → preprocessing → embeddings → FAISS retrieval → LLM answer → UI.
