"""Streamlit dashboard: stat tiles, tables, and the natural-language ask box.

A pure HTTP client (DESIGN.md D3) — it talks to the FastAPI service over httpx
and never imports the query layer, opens a Session, or holds the API key. Start
the API first; the base URL comes from API_BASE_URL.

Run: uv run uvicorn purdo.api.main:app --reload
     uv run streamlit run dashboard/app.py
"""
import os
from datetime import date

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API_BASE_URL", "http://localhost:8000")

TODAY = date(2026, 9, 1)          # demo date — real Sept data lives here


@st.cache_data(ttl=60)
def api_get(path, **params):
    """GET a query endpoint and return its rows. Cached so a keystroke in the
    ask box doesn't refetch all four panels."""
    r = httpx.get(f"{API}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


st.title("Purdo")
st.caption("Ontology-driven academic planner")

question = st.text_input("Ask about your degree")

if question:
    with st.spinner("Thinking..."):
        # the NL round trip runs Claude server-side, so it needs a long timeout
        r = httpx.post(f"{API}/ask", json={"question": question}, timeout=60)
        r.raise_for_status()
        result = r.json()
    st.write(result["answer"])
    st.caption(f"tool used: {result['tool_used']}")
    with st.expander("Raw data"):
        st.write(result["data"])


st.divider()

try:
    due = api_get("/assignments/due", today=TODAY.isoformat())
    exams = api_get("/exams/upcoming", today=TODAY.isoformat())
    short = api_get("/requirements/unsatisfied")
    blocked = api_get("/courses/blocked")
except httpx.HTTPError:
    st.error(f"Can't reach the API at {API}. Start it with:\n\n"
             "`uv run uvicorn purdo.api.main:app --reload`")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Due this week", len(due))
with c2:
    st.metric("Upcoming exams", len(exams))
with c3:
    st.metric("Requirements short", len(short))
with c4:
    st.metric("Blocked courses", len(blocked))

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Due this week")
    st.dataframe(due, use_container_width=True)

    st.subheader("Requirements short")
    st.dataframe(short, use_container_width=True)

with right:
    st.subheader("Upcoming exams")
    st.dataframe(exams, use_container_width=True)

    st.subheader("Blocked courses")
    if blocked:
        st.dataframe(blocked, use_container_width=True)
    else:
        st.success("No prerequisite conflicts — every planned course is unlocked.")
