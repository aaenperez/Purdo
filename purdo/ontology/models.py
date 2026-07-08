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
