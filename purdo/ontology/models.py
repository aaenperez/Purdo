"""Ontology objects and typed link tables.

- Six object types (Student, Semester, Course, Requirement, Assignment, Exam)
  plus four link tables that model relationships as first-class rows:
  ENROLLED_IN, SATISFIES, OFFERED_IN, and the self-referential PREREQUISITE_OF.
- Links carry their own properties — a grade belongs to a student's enrollment
  in a course, not to the course itself (DESIGN.md D1/D2). Assignment and Exam
  hang off Course by plain foreign key, since that containment is strictly
  one-to-many and carries no data of its own.
"""
from purdo.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
import enum

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    name: Mapped[str]
    credits: Mapped[int]

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

class Semester(Base):
    __tablename__ = "semesters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date]

class RequirementCategory(enum.Enum):
    CORE = "core"
    ELECTIVE = "elective"
    GEN_ED = "gen_ed"

class Requirement(Base):
    __tablename__ = "requirements"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category: Mapped[RequirementCategory]
    credits_needed: Mapped[int]

class AssignmentType(enum.Enum):
    HOMEWORK = "homework"
    QUIZ = "quiz"
    PROJECT = "project"

class AssignmentStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class ExamType(enum.Enum):
    MIDTERM = "midterm"
    FINAL = "final"

class EnrollmentStatus(enum.Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    PLANNED = "planned"

class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    status: Mapped[EnrollmentStatus]
    grade: Mapped[str | None]

class Assignment(Base):
    __tablename__ = "assignments"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    due_date: Mapped[date]
    type: Mapped[AssignmentType]
    status: Mapped[AssignmentStatus]

class Exam(Base):
    __tablename__ = "exams"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    date: Mapped[date]
    type: Mapped[ExamType]

    
class Satisfies(Base):
    __tablename__ = "satisfies"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirements.id"))
    credits_applied: Mapped[int]

class Offering(Base):
    __tablename__ = "offerings"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id"))

class Prerequisite(Base):
    __tablename__ = "prerequisites"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    prerequisite_course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))



