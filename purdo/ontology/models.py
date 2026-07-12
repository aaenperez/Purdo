"""Ontology object types and typed link tables (SQLAlchemy models).

YOU WRITE THIS (Lessons 2-3). Spec:

Objects:
- Student(id, name)
- Semester(id, name, start_date, end_date)
- Course(id, code, name, credits)
- Requirement(id, name, category: core|elective|gen_ed, credits_needed)
- Assignment(id, title, course_id, due_date, type: homework|quiz|project,
  status: todo|in_progress|done)
- Exam(id, title, course_id, date, type: midterm|final)

Typed link tables (see DESIGN.md D1/D2):
- enrollments:    Student ENROLLED_IN Course   + status, grade (link properties)
- satisfies:      Course SATISFIES Requirement + credits_applied
- offerings:      Course OFFERED_IN Semester
- prerequisites:  Course PREREQUISITE_OF Course (self-referential)
- (Assignment/Exam BELONGS_TO Course are plain FKs on those tables — discuss
  in Lesson 3 why that's OK for strict one-to-many containment.)

Use Python Enum classes for the category/type/status fields.
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



