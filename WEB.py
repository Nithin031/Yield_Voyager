import streamlit as st
from rag_backend import retrieve, generate_answer

st.title("Mini Legal RAG System")

query = st.text_input("Ask any ADVICE regarding LAW:")

if query:
    retrieved = retrieve(query, k=3)

    st.subheader("Retrieved Cases")
    for case, score in retrieved:
        st.markdown(f"**{case['case_name']}**  (score: {score:.3f})")
        st.write(case['case_outcome'])
        st.write("---")

    st.subheader("Answer")
    answer = generate_answer(query, retrieved)
    st.write(answer)
