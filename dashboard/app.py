"""Streamlit dashboard — pure HTTP client of the FastAPI query API.

YOU WRITE THIS (Lessons 10 & 12). Spec:
- httpx calls to http://localhost:8000 (base URL via env var).
- Cards/tables for: due this week, unsatisfied requirements, blocked courses,
  upcoming exams.
- An "Ask" text box that POSTs to /ask and renders the answer + the data.

Run: uv run streamlit run dashboard/app.py
"""
