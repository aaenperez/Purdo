"""HTTP layer over the query functions — not yet implemented.

- Planned: a read endpoint per query function, /ontology for schema
  introspection, and POST /ask for the natural-language layer.
- The dashboard currently calls purdo.queries.core in-process; because those
  functions already take a Session and return dicts, moving to HTTP is a change
  of transport rather than of logic.

Run: uv run uvicorn purdo.api.main:app --reload
"""
