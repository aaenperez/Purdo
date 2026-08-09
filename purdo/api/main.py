"""HTTP layer over the query functions.

- One read endpoint per query function, /ontology for schema introspection,
  and POST /ask for the natural-language layer.
- The query functions already take a Session and return dicts, so each route
  is a thin wrapper: this layer is transport, not logic.
- Sessions come from the db_session dependency, which closes them after the
  response is sent.

Run: uv run uvicorn purdo.api.main:app --reload
"""

from datetime import date

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from purdo.db import get_session
from purdo.nl.ask import ask
from purdo.ontology.registry import describe_ontology
from purdo.queries import core

app = FastAPI(
    title="Purdo",
    description="Ontology-driven academic planner.",
    version="0.1.0",
)


def db_session():
    """Yield a session per request; close it once the response is sent."""
    session = get_session()
    try:
        yield session
    finally:
        session.close()


class Requirement(BaseModel):
    requirement: str
    needed: int
    earned: int
    remaining: int


class Assignment(BaseModel):
    title: str
    course: str
    due: date
    type: str


class Exam(BaseModel):
    title: str
    course: str
    date: date
    type: str


class BlockedCourse(BaseModel):
    course: str
    missing_prereq: str


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    tool_used: str | None
    data: list | None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ontology")
def ontology(session=Depends(db_session)):
    """The registry as text — the same description the NL layer is primed with."""
    return {"ontology": describe_ontology(session)}


@app.get("/requirements/unsatisfied", response_model=list[Requirement])
def unsatisfied(session=Depends(db_session)):
    return core.unsatisfied_requirements(session)


@app.get("/assignments/due", response_model=list[Assignment])
def due(today: date | None = None, session=Depends(db_session)):
    return core.due_this_week(session, today or date.today())


@app.get("/exams/upcoming", response_model=list[Exam])
def exams(today: date | None = None, days: int = 28, session=Depends(db_session)):
    return core.upcoming_exams(session, today or date.today(), days)


@app.get("/courses/blocked", response_model=list[BlockedCourse])
def blocked(session=Depends(db_session)):
    return core.blocked_courses(session)


@app.post("/ask", response_model=AskResponse)
def ask_question(body: AskRequest, session=Depends(db_session)):
    """Free-text question -> Claude picks a query function -> grounded answer."""
    return ask(body.question, session)
