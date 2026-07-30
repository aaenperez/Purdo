"""Streamlit dashboard: stat tiles, tables, and the natural-language ask box.

Currently calls purdo.queries.core and purdo.nl.ask in-process. DESIGN.md D3
puts a FastAPI service on this boundary instead (httpx to localhost:8000); the
query functions already take a Session and return JSON-ready dicts, so that
swap is a change of transport, not of logic.

Run: uv run streamlit run dashboard/app.py
"""
import streamlit as st
from purdo.db import get_session
from purdo.nl.ask import ask
from datetime import date
from purdo.queries import core

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


session = get_session()
today = date(2026, 9, 1)          # demo date — real Sept data lives here

# run each query once, then render it twice (tile + table)
due = core.due_this_week(session, today)
exams = core.upcoming_exams(session, today)
short = core.unsatisfied_requirements(session)
blocked = core.blocked_courses(session)

st.divider()
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
