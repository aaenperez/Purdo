# Purdo — Ontology-Driven Academic Planner

A portfolio project modeling Purdue coursework the way Palantir Foundry models
real-world data: as **objects, properties, and relationships** — queryable in
natural language.

Instead of flat tables with incidental foreign keys, Purdo maintains an explicit
**ontology**: every object type (Course, Requirement, Exam, ...) and every link
type (ENROLLED_IN, SATISFIES, PREREQUISITE_OF, ...) is registered as first-class
metadata that the application — and the LLM query layer — can introspect.

## Architecture

```
┌─────────────┐   HTTP    ┌──────────────┐          ┌──────────────┐
│  Streamlit   │ ────────► │   FastAPI    │ ───────► │    SQLite    │
│  dashboard   │           │  query API   │          │  (SQLAlchemy)│
└─────────────┘           └──────┬───────┘          └──────────────┘
                                 │
                          ┌──────▼───────┐
                          │  Claude API  │  natural language → tool call
                          │  (tool use)  │  (never raw SQL generation)
                          └──────────────┘
```

- **Storage**: SQLite via SQLAlchemy. Typed link tables + an ontology registry,
  designed to migrate cleanly to Neo4j (every link table is an edge type).
- **Query layer**: FastAPI exposing fixed, tested query functions.
- **UI**: Streamlit dashboard calling the API over HTTP.
- **NL layer**: Claude with tool use — the model selects and parameterizes one of
  the fixed query functions; it never writes SQL.

## Ontology

Objects: `Student`, `Course`, `Requirement`, `Assignment`, `Exam`, `Semester`

Links (with properties where the relationship itself carries data):

| Link | Source → Target | Link properties |
|---|---|---|
| ENROLLED_IN | Student → Course | status (completed / in_progress / planned), grade |
| SATISFIES | Course → Requirement | credits_applied |
| OFFERED_IN | Course → Semester | — |
| PREREQUISITE_OF | Course → Course | — |
| BELONGS_TO | Assignment → Course | — |
| BELONGS_TO | Exam → Course | — |

See [DESIGN.md](DESIGN.md) for the reasoning behind each decision.

## Layout

```
purdo/
  db.py             # engine + session setup
  ontology/
    models.py       # object tables + typed link tables (SQLAlchemy)
    registry.py     # ontology metadata: object types + link types as data
    seed.py         # realistic seed data (Purdue CS junior)
  queries/
    core.py         # fixed query functions (due this week, unsatisfied reqs, ...)
  api/
    main.py         # FastAPI app
  nl/
    ask.py          # Claude tool-use layer: free text → query function call
dashboard/
  app.py            # Streamlit UI
```

## Running

```powershell
uv sync                                          # install deps
uv run python -m purdo.ontology.seed             # create + seed the DB
uv run uvicorn purdo.api.main:app --reload       # API at http://localhost:8000/docs
uv run streamlit run dashboard/app.py            # dashboard
```

Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` for the NL layer.

## Roadmap

- [ ] Phase 1: Schema + ontology registry + seed data
- [ ] Phase 2: Fixed query functions
- [ ] Phase 3: FastAPI + Streamlit dashboard
- [ ] Phase 4: Natural-language ask box (Claude tool use)
- [ ] Phase 5: Brightspace integration
- [ ] Phase 6: Neo4j migration
