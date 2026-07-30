"""Streamlit dashboard — pure HTTP client of the FastAPI query API.

YOU WRITE THIS (Lessons 10 & 12). Spec:
- httpx calls to http://localhost:8000 (base URL via env var).
- Cards/tables for: due this week, unsatisfied requirements, blocked courses,
  upcoming exams.
- An "Ask" text box that POSTs to /ask and renders the answer + the data.

Run: uv run streamlit run dashboard/app.py
"""
import streamlit as st
from purdo.db import get_session
from purdo.nl.ask import ask

st.title("Purdo")
st.caption("Ontology-driven academic planner")

question = st.text_input("Ask about your degree")

if question:
    with st.spinner("Thinking..."):
        result = ask(question)
    st.write(result["answer"])
    st.caption(f"tool used: {result['tool_used']}")
    with st.expander("Raw data"):
        st.write(result["data"])