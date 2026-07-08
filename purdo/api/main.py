"""FastAPI app exposing the query layer.

YOU WRITE THIS (Lesson 9). Spec:
- GET /queries/due-this-week
- GET /queries/unsatisfied-requirements
- GET /queries/blocked-courses
- GET /queries/upcoming-exams?days=14
- GET /ontology            -> the registry, so clients can introspect the schema
- POST /ask {"question": str} -> the NL layer (Lesson 11)
- Pydantic response models; session per request via FastAPI dependency.

Run: uv run uvicorn purdo.api.main:app --reload
"""
