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
from sqlalchemy import select, func, or_
from sqlalchemy.orm import aliased
from purdo.ontology.models import Assignment, Course, AssignmentStatus, Exam, Requirement, Satisfies, Enrollment, EnrollmentStatus, Prerequisite

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

def unsatisfied_requirements(session):
    # step 1: credits earned per requirement, counting only completed courses
    earned = (select(Satisfies.requirement_id,
                     func.sum(Satisfies.credits_applied).label("credits"))
              .join(Enrollment, Enrollment.course_id == Satisfies.course_id)
              .where(Enrollment.status == EnrollmentStatus.COMPLETED)
              .group_by(Satisfies.requirement_id)
              .subquery())

    # step 2: attach those totals to EVERY requirement, even ones with none
    stmt = (select(Requirement.name, Requirement.credits_needed,
                   func.coalesce(earned.c.credits, 0))
            .outerjoin(earned, earned.c.requirement_id == Requirement.id)
            .order_by(Requirement.name))

    return [{"requirement": name, "needed": needed, "earned": got,
             "remaining": needed - got}
            for name, needed, got in session.execute(stmt)
            if got < needed]

def blocked_courses(session):
    Prereq = aliased(Course)
    PrereqEnr = aliased(Enrollment)
    stmt = (select(Course.code, Prereq.code)
            .join(Enrollment, Enrollment.course_id == Course.id)
            .join(Prerequisite, Prerequisite.course_id == Course.id)
            .join(Prereq, Prerequisite.prerequisite_course_id == Prereq.id)
            .outerjoin(PrereqEnr,PrereqEnr.course_id == Prereq.id)
            .where(Enrollment.status == EnrollmentStatus.PLANNED)
            .where(or_(PrereqEnr.status != EnrollmentStatus.COMPLETED,
                       PrereqEnr.status == None)))
    return list(session.execute(stmt))