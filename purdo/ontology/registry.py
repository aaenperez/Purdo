"""The ontology registry: the schema stored as queryable data.

- ObjectType and LinkType rows describe every object and relationship in the
  model, including which properties each link carries.
- `describe_ontology()` renders that into text used as the natural-language
  layer's system prompt, so the schema has exactly one source of truth.
"""

from purdo.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select

class ObjectType(Base):
    __tablename__ = "object_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    table_name: Mapped[str]
    description: Mapped[str]

class LinkType(Base):
    __tablename__ = "link_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    table_name: Mapped[str]
    description: Mapped[str]
    source_type: Mapped[str]
    target_type: Mapped[str]
    properties: Mapped[str | None]

def register_ontology(session):
    session.add_all([
        ObjectType(
            name="Student",
            table_name="students",
            description="A person enrolled at the university.",
        ),
        ObjectType(
            name="Course",
            table_name="courses",
            description="A university course with a code, name, and credit count.",
        ),
        ObjectType(
            name="Semester",
            table_name="semesters",
            description="An academic term with start and end dates.",
        ),
        ObjectType(
            name="Requirement",
            table_name="requirements",
            description="A degree requirement (core, elective, or gen-ed) needing a number of credits.",
        ),
        ObjectType(
            name="Assignment",
            table_name="assignments",
            description="Gradable coursework (homework, quiz, or project) with a due date and status.",
        ),
        ObjectType(
            name="Exam",
            table_name="exams",
            description="A midterm or final exam for a course on a specific date.",
        ),
        LinkType(
            name="ENROLLED_IN",
            source_type="Student",
            target_type="Course",
            table_name="enrollments",
            description="The student takes the course; the link records how it went.",
            properties="status, grade",
        ),
        LinkType(
            name="SATISFIES",
            source_type="Course",
            target_type="Requirement",
            table_name="satisfies",
            description="Completing the course counts credits toward the requirement.",
            properties="credits_applied",
        ),
        LinkType(
            name="OFFERED_IN",
            source_type="Course",
            target_type="Semester",
            table_name="offerings",
            description="The course is offered during the semester.",
        ),
        LinkType(
            name="PREREQUISITE_OF",
            source_type="Course",
            target_type="Course",
            table_name="prerequisites",
            description="The prerequisite course must be completed before the target course.",
        ),
        LinkType(
            name="ASSIGNMENT_BELONGS_TO",
            source_type="Assignment",
            target_type="Course",
            table_name="assignments",
            description="The assignment is part of the course (stored as a foreign key on assignments).",
        ),
        LinkType(
            name="EXAM_BELONGS_TO",
            source_type="Exam",
            target_type="Course",
            table_name="exams",
            description="The exam is part of the course (stored as a foreign key on exams).",
        ),
    ])
    session.commit()

def describe_ontology(session):
    lines = []
    lines.append("OBJECT TYPES:")
    for o in session.scalars(select(ObjectType)):
        lines.append(f"- {o.name} (table: {o.table_name}): {o.description}")
    lines.append("LINK TYPES:")
    for l in session.scalars(select(LinkType)):
        lines.append(f"- {l.source_type} -{l.name}-> {l.target_type} "
                     f"[{l.properties}]: {l.description}")
    return "\n".join(lines)
