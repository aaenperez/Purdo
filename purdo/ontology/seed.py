"""Seed script: create tables and load Aaen's real transcript.

Data source: Purdue degree audit (2026-07-19) + myPurdue catalog prereqs.
Simplifications: OR-prerequisites reduced to the path actually taken;
Fall 2026 assignments/exams are plausible placeholders until Brightspace.

Run: uv run python -m purdo.ontology.seed
"""
from datetime import date

from purdo.db import engine, Base, get_session
from purdo.ontology.models import (Student, Semester, Course, Requirement,
    Enrollment, Satisfies, Offering, Prerequisite, RequirementCategory,
    EnrollmentStatus, Assignment, Exam, AssignmentType, AssignmentStatus, ExamType)
from purdo.ontology.registry import register_ontology

SEMESTERS = {
    # name: (start, end). Summer 2024 = AP/transfer credit bucket, not attended.
    "Summer 2024": (date(2024, 6, 10), date(2024, 8, 3)),
    "Fall 2024": (date(2024, 8, 19), date(2024, 12, 14)),
    "Spring 2025": (date(2025, 1, 13), date(2025, 5, 10)),
    "Fall 2025": (date(2025, 8, 25), date(2025, 12, 20)),
    "Spring 2026": (date(2026, 1, 12), date(2026, 5, 9)),
    "Fall 2026": (date(2026, 8, 24), date(2026, 12, 19)),
    "Spring 2027": (date(2027, 1, 11), date(2027, 5, 8)),
    "Fall 2027": (date(2027, 8, 23), date(2027, 12, 18)),
    "Spring 2028": (date(2028, 1, 10), date(2028, 5, 6)),
}

COURSES = {
    # code: (name, credits)
    "ENGL 10600": ("First-Year Composition", 4),
    "STAT 30100": ("Elementary Statistical Methods", 3),
    "HIST 10500": ("Global History", 3),
    "MA 16500": ("Analytic Geometry & Calculus I", 4),
    "CS 1XXXX": ("Computer Science Principles (AP)", 3),
    "PHYS 1XXXX": ("Physics C: Mechanics (AP)", 3),
    "CS 18000": ("Problem Solving & Object-Oriented Programming", 4),
    "CS 19300": ("Tools", 1),
    "ECON 21000": ("Principles of Economics", 3),
    "EAPS 10600": ("Geosciences Cinema", 3),
    "MA 16200": ("Plane Analytic Geometry & Calculus II", 5),
    "SCLA 10200": ("Critical Thinking & Communication II", 3),
    "CS 18200": ("Foundations of Computer Science", 3),
    "CS 24000": ("Programming in C", 3),
    "MA 26100": ("Multivariate Calculus", 4),
    "EAPS 11100": ("Physical Geology", 3),
    "MA 26500": ("Linear Algebra", 3),
    "CS 25000": ("Computer Architecture", 4),
    "CS 25100": ("Data Structures and Algorithms", 3),
    "HIST 15200": ("United States Since 1877", 3),
    "EAPS 11200": ("Earth Through Time", 3),
    "CS 25200": ("Systems Programming", 4),
    "STAT 35000": ("Introduction to Statistics", 3),
    "POL 32700": ("Global Green Politics", 3),
    "ANTH 10000": ("Being Human: Intro to Anthropology", 3),
    "CS 38100": ("Introduction to Analysis of Algorithms", 3),
    "CS 44800": ("Introduction to Relational Database Systems", 3),
    "ENGL 30400": ("Advanced Composition", 3),
    "ANTH 21000": ("Technology and Culture", 3),
    "VIP 37920": ("Junior Participation in VIP", 2),
    "CS 37300": ("Data Mining and Machine Learning", 3),
    "CS 47100": ("Introduction to Artificial Intelligence", 3),
    "STAT 41600": ("Probability", 3),
    "CS 35400": ("Operating Systems", 3),
}

COMPLETED = [
    # (semester, code, grade) — "TR" = AP/transfer credit
    ("Summer 2024", "ENGL 10600", "TR"),
    ("Summer 2024", "STAT 30100", "TR"),
    ("Summer 2024", "HIST 10500", "TR"),
    ("Summer 2024", "MA 16500", "TR"),
    ("Summer 2024", "CS 1XXXX", "TR"),
    ("Summer 2024", "PHYS 1XXXX", "TR"),
    ("Fall 2024", "CS 18000", "B"),
    ("Fall 2024", "CS 19300", "A"),
    ("Fall 2024", "ECON 21000", "A+"),
    ("Fall 2024", "EAPS 10600", "A+"),
    ("Fall 2024", "MA 16200", "B-"),
    ("Spring 2025", "SCLA 10200", "A+"),
    ("Spring 2025", "CS 18200", "B"),
    ("Spring 2025", "CS 24000", "C"),
    ("Spring 2025", "MA 26100", "B+"),
    ("Fall 2025", "EAPS 11100", "A+"),
    ("Fall 2025", "MA 26500", "A-"),
    ("Fall 2025", "CS 25000", "B-"),
    ("Fall 2025", "CS 25100", "B-"),
    ("Fall 2025", "HIST 15200", "A"),
    ("Spring 2026", "EAPS 11200", "A+"),
    ("Spring 2026", "CS 25200", "A"),
    ("Spring 2026", "STAT 35000", "A"),
    ("Spring 2026", "POL 32700", "A"),
    ("Spring 2026", "ANTH 10000", "A+"),
]

IN_PROGRESS = [
    ("Fall 2026", "CS 38100"),
    ("Fall 2026", "CS 44800"),
    ("Fall 2026", "ENGL 30400"),
    ("Fall 2026", "ANTH 21000"),
    ("Fall 2026", "VIP 37920"),
]

PLANNED = [
    ("Spring 2027", "CS 37300"),
    ("Spring 2027", "CS 47100"),
    ("Fall 2027", "STAT 41600"),
    ("Fall 2027", "CS 35400"),
]

REQUIREMENTS = {
    # name: (category, credits_needed)
    "Degree Total": (RequirementCategory.CORE, 120),
    "Upper-Level Credits": (RequirementCategory.CORE, 32),
    "CS Major Core": (RequirementCategory.CORE, 46),
    "University Core Curriculum": (RequirementCategory.GEN_ED, 26),
    "Other Departmental": (RequirementCategory.CORE, 16),
    "College of Science": (RequirementCategory.GEN_ED, 12),
    "Machine Intelligence Track": (RequirementCategory.ELECTIVE, 18),
}

SATISFIES = {
    # requirement: [course codes]
    "CS Major Core": ["CS 18000", "CS 18200", "CS 24000", "CS 25000",
                      "CS 25100", "CS 25200", "MA 26100", "MA 26500"],
    "University Core Curriculum": ["ENGL 10600", "SCLA 10200", "STAT 30100",
                                   "EAPS 11100", "EAPS 11200", "HIST 10500",
                                   "ECON 21000", "MA 16500", "EAPS 10600"],
    "Other Departmental": ["MA 16200", "STAT 35000", "PHYS 1XXXX"],
    "College of Science": ["ENGL 30400", "POL 32700", "HIST 15200",
                           "ANTH 10000", "ANTH 21000"],
    "Machine Intelligence Track": ["CS 37300", "CS 38100", "CS 47100",
                                   "STAT 41600"],
    "Upper-Level Credits": ["CS 38100", "CS 44800", "ENGL 30400", "POL 32700",
                            "CS 37300", "CS 47100", "STAT 41600", "CS 35400"],
}

PREREQS = [
    # (prerequisite, course) — verified against myPurdue catalog 2026-07-19
    ("CS 18000", "CS 18200"),
    ("CS 18000", "CS 24000"),
    ("CS 18200", "CS 25000"),
    ("CS 24000", "CS 25000"),
    ("CS 18200", "CS 25100"),
    ("CS 24000", "CS 25100"),
    ("CS 25000", "CS 25200"),
    ("CS 25100", "CS 25200"),
    ("CS 25100", "CS 38100"),
    ("MA 26100", "CS 38100"),
    ("CS 25100", "CS 44800"),
    ("CS 25100", "CS 47100"),
    ("CS 18200", "CS 37300"),
    ("CS 25100", "CS 37300"),
    ("STAT 35000", "CS 37300"),
    ("CS 25200", "CS 35400"),
]

ASSIGNMENTS = [
    # (code, title, type, due, status) — placeholders until Brightspace
    ("CS 38100", "Homework 1", AssignmentType.HOMEWORK, date(2026, 9, 4), AssignmentStatus.TODO),
    ("CS 38100", "Homework 2", AssignmentType.HOMEWORK, date(2026, 9, 18), AssignmentStatus.TODO),
    ("CS 44800", "Quiz 1", AssignmentType.QUIZ, date(2026, 9, 11), AssignmentStatus.TODO),
    ("CS 44800", "Project 1: SQL", AssignmentType.PROJECT, date(2026, 9, 25), AssignmentStatus.TODO),
    ("ENGL 30400", "Essay 1", AssignmentType.HOMEWORK, date(2026, 9, 30), AssignmentStatus.TODO),
    ("ANTH 21000", "Reading Response 1", AssignmentType.HOMEWORK, date(2026, 9, 9), AssignmentStatus.TODO),
    ("VIP 37920", "Project Proposal", AssignmentType.PROJECT, date(2026, 9, 21), AssignmentStatus.TODO),
]

EXAMS = [
    # (code, title, type, date)
    ("CS 38100", "Midterm 1", ExamType.MIDTERM, date(2026, 10, 8)),
    ("CS 44800", "Midterm 1", ExamType.MIDTERM, date(2026, 10, 15)),
    ("CS 38100", "Final Exam", ExamType.FINAL, date(2026, 12, 14)),
    ("CS 44800", "Final Exam", ExamType.FINAL, date(2026, 12, 16)),
]


def seed():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = get_session()
    register_ontology(session)

    me = Student(name="Aaen Perez")
    semesters = {name: Semester(name=name, start_date=s, end_date=e)
                 for name, (s, e) in SEMESTERS.items()}
    courses = {code: Course(code=code, name=name, credits=cr)
               for code, (name, cr) in COURSES.items()}
    requirements = {name: Requirement(name=name, category=cat, credits_needed=cr)
                    for name, (cat, cr) in REQUIREMENTS.items()}
    session.add(me)
    session.add_all(semesters.values())
    session.add_all(courses.values())
    session.add_all(requirements.values())
    session.flush()  # assigns ids so the link rows below can reference them

    links = []
    for sem, code, grade in COMPLETED:
        links.append(Enrollment(student_id=me.id, course_id=courses[code].id,
                                status=EnrollmentStatus.COMPLETED, grade=grade))
        links.append(Offering(course_id=courses[code].id, semester_id=semesters[sem].id))
    for sem, code in IN_PROGRESS:
        links.append(Enrollment(student_id=me.id, course_id=courses[code].id,
                                status=EnrollmentStatus.IN_PROGRESS))
        links.append(Offering(course_id=courses[code].id, semester_id=semesters[sem].id))
    for sem, code in PLANNED:
        links.append(Enrollment(student_id=me.id, course_id=courses[code].id,
                                status=EnrollmentStatus.PLANNED))
        links.append(Offering(course_id=courses[code].id, semester_id=semesters[sem].id))
    for req, codes in SATISFIES.items():
        for code in codes:
            links.append(Satisfies(course_id=courses[code].id,
                                   requirement_id=requirements[req].id,
                                   credits_applied=COURSES[code][1]))
    for prereq, code in PREREQS:
        links.append(Prerequisite(course_id=courses[code].id,
                                  prerequisite_course_id=courses[prereq].id))
    for code, title, kind, due, status in ASSIGNMENTS:
        links.append(Assignment(title=title, course_id=courses[code].id,
                                due_date=due, type=kind, status=status))
    for code, title, kind, when in EXAMS:
        links.append(Exam(title=title, course_id=courses[code].id,
                          date=when, type=kind))
    session.add_all(links)
    session.commit()

    print(f"seeded: {len(courses)} courses, "
          f"{len(COMPLETED) + len(IN_PROGRESS) + len(PLANNED)} enrollments, "
          f"{len(PREREQS)} prereq edges, {len(requirements)} requirements")
    session.close()


if __name__ == "__main__":
    seed()
