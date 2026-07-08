# Design Decisions

This file records *why* the project is built the way it is. Every entry should be
defensible in an interview. Extended after each lesson.

## D1 — Typed link tables + ontology registry (not a generic edge table, not plain FKs)

**Decision**: Each relationship type gets its own table (`enrollments`,
`prerequisites`, ...), and a separate **registry** (`object_types`, `link_types`
metadata tables) describes the whole ontology as queryable data.

**Why**:
- Plain foreign keys make relationships implicit — nothing in the system *knows*
  "ENROLLED_IN" is a concept. That contradicts the project's premise.
- A single generic `edges` table (triple-store style) is maximally graph-like but
  loses referential integrity (nothing stops a nonsense edge) and makes every SQL
  query filter on source_type/target_type.
- Typed tables keep SQL clean and constraint-enforced, while the registry makes
  the ontology introspectable — the NL layer reads the ontology instead of having
  it hardcoded. This mirrors how Foundry separates the ontology layer from
  storage.
- Neo4j migration: each link table maps 1:1 to an edge type; the registry becomes
  the graph schema.

## D2 — Link properties

**Decision**: Relationships can carry their own fields. `ENROLLED_IN` has
`status` (completed / in_progress / planned) and `grade`; `SATISFIES` has
`credits_applied`.

**Why**: Enrollment status describes neither the student nor the course — it
describes the *link between them*. It's also load-bearing: "which requirements
are unsatisfied" and "which courses are blocked by prereqs" are unanswerable
without knowing which courses are completed. Foundry calls these link properties.

## D3 — Streamlit → FastAPI over HTTP

**Decision**: Two processes. Streamlit is a pure client calling the FastAPI query
API with httpx.

**Why**: Realistic client/server separation; the OpenAPI docs page is a demo
artifact; the NL layer (and the API key) live server-side where they belong.
Trade-off accepted: two processes to run in dev.

## D4 — NL via tool use, not text-to-SQL

**Decision**: Claude receives the ontology description + a set of tools that map
1:1 to fixed, tested query functions. It picks and parameterizes a tool; it never
emits SQL.

**Why**: Safety (no injection surface, no unbounded queries), reliability (the
functions are tested; the model only routes), and honesty in the demo (failure
mode is "I can't answer that" instead of silently wrong SQL).
