from src.models import *

import random

import os
from sqlalchemy import create_engine, select
from dotenv import load_dotenv

from sqlalchemy.orm import Session

from faker import Faker

fake = Faker()

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:{os.getenv("POSTGRES_PORT")}/{os.getenv('POSTGRES_DB')}",
    echo=True,
)

SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Literature",
    "Geography",
    "History",
    "Biology",
    "Astronomy",
]


def seed():
    with Session(engine) as session:
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Student).delete()
        session.query(Group).delete()
        session.query(Grade).delete()

        teachers = []

        for _ in range(5):
            teachers.append(
                Teacher(first_name=fake.first_name(), last_name=fake.last_name())
            )
        session.add_all(teachers)
        session.flush()

        subjects = []
        for i in range(len(teachers)):
            subjects.append(Subject(name=SUBJECTS[i], teacher_id=teachers[i].id))

        for i in range(len(teachers), len(SUBJECTS)):
            random_teacher = random.choice(teachers)
            subjects.append(Subject(name=SUBJECTS[i], teacher_id=random_teacher.id))

        session.add_all(subjects)
        session.flush()

        groups = []
        for _ in range(3):
            groups.append(
                Group(name=str(f"{fake.word().upper()}-{fake.safe_color_name()}"))
            )
        session.add_all(groups)
        session.flush()

        students = []
        groups_db = session.query(Group).all()
        groups_db_ids = []
        for group in groups_db:
            groups_db_ids.append(group.id)

        for i in range(45):
            current_group_id = groups_db_ids[i // 15]
            students.append(
                Student(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    group_id=current_group_id,
                )
            )
        session.add_all(students)
        session.flush()

        grades = []
        students_db = session.scalars(select(Student)).all()
        subjects_db = session.scalars(select(Subject)).all()

        for student in students_db:
            for i in range(20):
                fake_grade_date = fake.date_time_between(
                    start_date="-30d", end_date="now"
                )
                random_grade = random.choice(range(60, 100))
                random_subject = random.choice(subjects_db)
                grades.append(
                    Grade(
                        grade=random_grade,
                        grade_date=fake_grade_date,
                        student_id=student.id,
                        subject_id=random_subject.id,
                    )
                )
        session.add_all(grades)
        session.commit()


if __name__ == "__main__":
    seed()
