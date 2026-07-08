"""Seed script: create tables and load realistic data.

YOU WRITE THIS (Lesson 5). Spec:
- Drop/create all tables, register the ontology, then insert:
  - One student (you), CS major at Purdue, junior year.
  - Semesters: past ones (completed courses), current (Fall 2026), next.
  - Completed courses (e.g. CS180, CS182, CS240, CS250, CS251, MA261...),
    in-progress courses (e.g. CS252, STAT350, ...), planned courses
    (e.g. CS381, CS448...) — with matching ENROLLED_IN statuses.
  - Requirements (core/elective/gen-ed) with realistic credit counts, wired
    to courses via SATISFIES.
  - Prerequisite edges (e.g. CS250 & CS251 -> CS252, CS182 -> CS240 ...).
  - Assignments and exams for in-progress courses with due dates around
    "today" so the Phase 2 queries return interesting results.
- Runnable as: uv run python -m purdo.ontology.seed
"""
