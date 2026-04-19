from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from src.models import *
from src.configuration import engine

# Зробити наступні вибірки з отриманої бази даних:
#
# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
# 2. Знайти студента із найвищим середнім балом з певного предмета.
# 3. Знайти середній бал у групах з певного предмета.
# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
# 5. Знайти які курси читає певний викладач.
# 6. Знайти список студентів у певній групі.
# 7. Знайти оцінки студентів у окремій групі з певного предмета.
# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
# 9. Знайти список курсів, які відвідує певний студент.
# 10. Список курсів, які певному студенту читає певний викладач.


def select_1():
    with Session(engine) as session:
        result_query = (
            select(
                Student.first_name,
                Student.last_name,
                func.round(func.avg(Grade.grade), 3).label("avg_grade"),
            )
            .join(Grade)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(5)
        )
        result = session.execute(result_query).all()

        for i in result:
            print(f"{i.first_name} {i.last_name}: {i.avg_grade}")


def select_2(subject_name: str):
    with Session(engine) as session:
        result_query = (
            select(
                Student.first_name,
                Student.last_name,
                func.round(func.avg(Grade.grade), 3).label("avg_grade"),
            )
            .select_from(Student)
            .join(Grade)
            .join(Subject)
            .where(Subject.name == subject_name)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(1)
        )
        result = session.execute(result_query).first()
        print(
            f"{result.first_name} {result.last_name} (Average grade: {result.avg_grade})"
        )


def select_3(subject_name: str):
    with Session(engine) as session:
        result_query = (
            select(Group.name, func.round(func.avg(Grade.grade), 3).label("avg_grade"))
            .select_from(Group)
            .join(Student)
            .join(Grade)
            .join(Subject)
            .where(Subject.name == subject_name)
            .group_by(Group.id)
            .order_by(desc("avg_grade"))
        )
        result = session.execute(result_query).all()
        for i in result:
            print(f"Group {i.name}: {i.avg_grade}")


def select_4():
    with Session(engine) as session:
        result_query = select(func.round(func.avg(Grade.grade), 3).label("avg_grade"))
        result = session.execute(result_query).scalar()

        print(f"\nOverall average grade across all grades: {result}")


def select_5(teacher_first_name: str, teacher_last_name: str):
    with Session(engine) as session:
        result_query = (
            select(Subject.name)
            .join(Teacher)
            .where(Teacher.first_name == teacher_first_name)
            .where(Teacher.last_name == teacher_last_name)
            .group_by(Subject.id)
        )

        result = session.execute(result_query).all()
        for i in result:
            print(f"{i.name}")


# find teacher by id version
def select_5_by_id(teacher_id: int):
    with Session(engine) as session:
        result_query = (
            select(Subject.name)
            .join(Teacher)
            .where(Teacher.id == teacher_id)
            .group_by(Subject.id)
        )
        result = session.execute(result_query).all()
        for i in result:
            print(f"{i.name}")


def select_6(group_name: str):
    with Session(engine) as session:
        result_query = (
            select(Student.first_name, Student.last_name)
            .join(Group)
            .where(Group.name == group_name)
            .group_by(Student.id)
        )
        result = session.execute(result_query).all()
        for i in result:
            print(f"{i.first_name} {i.last_name}")


# find students in group by id version
def select_6_by_id(group_id: int):
    with Session(engine) as session:
        result_query = (
            select(Student.first_name, Student.last_name)
            .join(Group)
            .where(Group.id == group_id)
            .group_by(Student.id)
        )
        result = session.execute(result_query).all()
        for i in result:
            print(f"{i.first_name} {i.last_name}")


def select_7(group_name: str, subject_name: str):
    with Session(engine) as session:
        result_query = (
            (select(Student.first_name, Student.last_name, Grade.grade))
            .select_from(Student)
            .join(Grade)
            .join(Subject)
            .join(Group)
            .where((Group.name == group_name) & (Subject.name == subject_name))
        )
        result = session.execute(result_query).all()
        for i in result:
            print(f"{i.first_name} {i.last_name}: {i.grade}")


def select_8(teacher_first_name: str, teacher_last_name: str):
    with Session(engine) as session:
        result_query = (
            select(
                Teacher.first_name,
                Teacher.last_name,
                func.round(func.avg(Grade.grade), 3).label("avg_grade"),
            )
            .select_from(Teacher)
            .join(Subject)
            .join(Grade)
            .where(
                (Teacher.first_name == teacher_first_name)
                & (Teacher.last_name == teacher_last_name)
            )
            .group_by(Teacher.id)
        )

        result = session.execute(result_query).first()
        if result:
            print(
                f"\nAverage grade given by {result.first_name} {result.last_name}: {result.avg_grade}"
            )


def select_8_by_id(teacher_id: int):
    with Session(engine) as session:
        result_query = (
            (
                select(
                    Teacher.first_name,
                    Teacher.last_name,
                    func.round(func.avg(Grade.grade), 3).label("avg_grade"),
                )
            )
            .select_from(Teacher)
            .join(Subject)
            .join(Grade)
            .where(Teacher.id == teacher_id)
            .group_by(Teacher.id)
        )
        result = session.execute(result_query).first()
        if result:
            print(
                f"\nAverage grade given by {result.first_name} {result.last_name}: {result.avg_grade}"
            )


def select_9(student_id: int):
    with Session(engine) as session:
        result_query = (
            select(Subject.name)
            .select_from(Grade)
            .join(Subject)
            .join(Student)
            .where(Student.id == student_id)
            .distinct()
        )

        result = session.execute(result_query).scalars().all()
        for course in result:
            print(f"{course}")


def select_10(teacher_id: int, student_id: int):
    with Session(engine) as session:
        result_query = (
            select(Subject.name)
            .select_from(Student)
            .join(Grade)
            .join(Subject)
            .join(Teacher)
            .where((Teacher.id == teacher_id) & (Student.id == student_id))
            .distinct()
        )

        result = session.execute(result_query).scalars().all()
        for course in result:
            print(f"- {course}")


def select_additional_1(teacher_id: int, student_id: int):
    with Session(engine) as session:
        result_query = (
            select(func.round(func.avg(Grade.grade), 3).label("avg_grade"))
            .select_from(Grade)
            .join(Subject)
            .where(
                (Subject.teacher_id == teacher_id) & (Grade.student_id == student_id)
            )
        )

        result = session.execute(result_query).scalar()
        print(
            f"\nAverage grade given by teacher ID {teacher_id} to student ID {student_id}: {result}"
        )


def select_additional_2(group_id: int, subject_id: int):
    with Session(engine) as session:
        subquery = (
            select(func.max(Grade.grade_date))
            .join(Student)
            .where((Grade.subject_id == subject_id) & (Student.group_id == group_id))
            .scalar_subquery()
        )

        result_query = (
            select(Student.first_name, Student.last_name, Grade.grade, Grade.grade_date)
            .select_from(Grade)
            .join(Student)
            .where(
                (Grade.subject_id == subject_id)
                & (Student.group_id == group_id)
                & (Grade.grade_date == subquery)
            )
        )

        results = session.execute(result_query).all()
        if results:
            print(
                f"\nGrades of group {group_id} in subject {subject_id} on the last lesson ({results[0].grade_date}):"
            )
            for i in results:
                print(f"- {i.first_name} {i.last_name}: {i.grade}")


if __name__ == "__main__":
    pass
    # select_1()
    # select_2("Physics")
    # select_3("Physics")
    # select_4()
    # select_5("Bradley", "Drake")
    # select_5_by_id(136)
    # select_6("CAREER-black")
    # select_6_by_id(28)
    # select_7("CAREER-black", "Physics")
    # select_8("Amber", "Gonzales")
    # select_8_by_id(137)
    # select_9(220)
    # select_10(136, 211)
    # select_additional_1(138, 221)
    # select_additional_2(28, 123)
