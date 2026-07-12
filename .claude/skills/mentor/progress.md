# Purdo learning log

Current lesson: **L2 — object models in models.py**

## Weekly schedule (set 2026-07-09; ~3 sessions/week, adjust if a week slips)

| Week | Dates | Lessons | Milestone — "done" means |
|---|---|---|---|
| 1 | Jul 9 – Jul 15 | L1, L2, L3 | Schema exists: `create_all` builds every object + link table |
| 2 | Jul 16 – Jul 22 | L4, L5 | Seeded DB with real transcript; ontology introspectable; tag v0.1 |
| 3 | Jul 23 – Jul 29 | L6, L7, L8 | All four query functions answer correctly against seed data |
| 4 | Jul 30 – Aug 5 | L9, L10 | Dashboard demo: Streamlit → FastAPI → SQLite end to end; tag v0.2 |
| 5 | Aug 6 – Aug 12 | L11, L12 | NL ask box works; README screenshots; mock interview passed; tag v1.0 |
| — | Aug 13 – Aug 19 | buffer | Slack for slippage, else start Brightspace research (Phase 5) |

Rule: a week's milestone must pass its checkpoint questions before the next
week starts — schedule slips, quality doesn't.

| Lesson | Status | Date | Notes |
|---|---|---|---|
| L1 db.py | done | 2026-07-10 | Debugged package-name + string-vs-variable errors well. CHECKPOINT NOT PASSED: asked for answers instead of answering (one-engine/many-sessions, lazy connect, single Base) — RE-ASK at start of L2 before teaching. |
| L2 object models | not started | | |
| L3 link tables | not started | | |
| L4 registry | not started | | |
| L5 seed data | not started | | |
| L6 due/exams queries | not started | | |
| L7 unsatisfied reqs | not started | | |
| L8 blocked courses | not started | | |
| L9 FastAPI | not started | | |
| L10 Streamlit | not started | | |
| L11 Claude tool use | not started | | |
| L12 ask box + polish | not started | | |

## Struggles / revisit
(nothing yet)

## Takeovers (code Claude wrote instead of the user)
- 2026-07-10 (L2 step 4): 3 enums + Assignment/Exam models — repetitive-pattern
  takeover at user's request (rule 2 amended same day). User had written the
  enum + model patterns himself in steps 1-3; ForeignKey was newly taught but
  not yet typed by him. Spot-check FK understanding at L3 start.
