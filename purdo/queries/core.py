"""Fixed query functions — the only way data is ever read.

YOU WRITE THIS (Lessons 6-8). These are plain functions taking a Session and
returning plain dicts/lists (JSON-serializable), so FastAPI, Streamlit, and the
Claude tool-use layer can all share them. Spec:

- due_this_week(session) -> assignments due in the next 7 days, across all
  in-progress courses, sorted by due date.
- unsatisfied_requirements(session) -> requirements where completed credits
  (via SATISFIES links from completed enrollments) < credits_needed, with the
  remaining-credit gap.
- blocked_courses(session) -> planned courses having at least one
  PREREQUISITE_OF edge from a course that is not completed; include which
  prereqs are missing.
- upcoming_exams(session, days: int = 14) -> exams within the window for
  in-progress courses.
"""

from datetime import timedelta
from sqlalchemy import select
from purdo.ontology.models import Assignment, Course, AssignmentStatus, Exam

def due_this_week(session, today):
    end = timedelta(7) + today
    stmt = (select(Assignment, Course)
            .join(Course, Assignment.course_id == Course.id)
            .where(Assignment.due_date >= today)
            .where(Assignment.due_date <= end)
            .where(Assignment.status == AssignmentStatus.TODO)
            .order_by(Assignment.due_date))
    return list(session.execute(stmt))

def upcoming_exams(session, today, days = 28):
    end = timedelta(days) + today
    stmt = (select(Exam, Course)
            .join(Course, Exam.course_id == Course.id)
            .where(Exam.date >= today)
            .where(Exam.date <= end)
            .order_by(Exam.date))
    return list(session.execute(stmt))