import argparse
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Group, Student, Teacher, Subject, Grade
from src.configuration import engine

MODELS_MAP = {
    "Group": Group,
    "Student": Student,
    "Teacher": Teacher,
    "Subject": Subject,
    "Grade": Grade,
}


def parse_args():
    parser = argparse.ArgumentParser(description="CLI CRUD app for University Database")

    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action to perform",
    )
    parser.add_argument(
        "-m", "--model", choices=MODELS_MAP.keys(), required=True, help="Target model"
    )

    parser.add_argument("--id", type=int, help="Record ID (required for update/remove)")
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Name of group/subject OR 'First Last' name for person",
    )

    parser.add_argument("--email", type=str, help="Email for Student")
    parser.add_argument("--group_id", type=int, help="Group ID for Student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for Subject")
    parser.add_argument("--student_id", type=int, help="Student ID for Grade")
    parser.add_argument("--subject_id", type=int, help="Subject ID for Grade")
    parser.add_argument("--grade", type=int, help="Grade value (int)")
    parser.add_argument(
        "--grade_date", type=str, help="Date for Grade in YYYY-MM-DD format"
    )

    return parser.parse_args()


def handle_create(session: Session, args):
    model_class = MODELS_MAP[args.model]

    obj = None

    if args.model == "Teacher":
        first_name, last_name = args.name.split(" ", 1)
        obj = model_class(first_name=first_name, last_name=last_name)

    elif args.model == "Student":
        first_name, last_name = args.name.split(" ", 1)
        obj = model_class(
            first_name=first_name,
            last_name=last_name,
            email=args.email or f"{first_name.lower()}@test.com",
            group_id=args.group_id,
        )

    elif args.model == "Group":
        obj = model_class(name=args.name)

    elif args.model == "Subject":
        obj = model_class(name=args.name, teacher_id=args.teacher_id)

    elif args.model == "Grade":
        date_obj = (
            datetime.strptime(args.grade_date, "%Y-%m-%d").date()
            if args.grade_date
            else datetime.now().date()
        )
        obj = model_class(
            grade=args.grade,
            grade_date=date_obj,
            subject_id=args.subject_id,
            student_id=args.student_id,
        )

    session.add(obj)
    session.commit()
    print(f"✅ {args.model} created successfully with ID: {obj.id}")


def handle_list(session: Session, args):
    model_class = MODELS_MAP[args.model]
    records = session.scalars(select(model_class)).all()

    print(f"--- List of {args.model}s ---")
    for r in records:
        if args.model in ["Teacher", "Student"]:
            print(f"ID: {r.id} | {r.first_name} {r.last_name}")
        elif args.model in ["Group", "Subject"]:
            print(f"ID: {r.id} | {r.name}")
        elif args.model == "Grade":
            print(
                f"ID: {r.id} | Grade: {r.grade} | Date: {r.grade_date} | Student ID: {r.student_id} | Subject ID: {r.subject_id}"
            )


def handle_update(session: Session, args):
    if not args.id:
        print("Error: --id is required for update action.")
        return

    model_class = MODELS_MAP[args.model]
    obj = session.get(model_class, args.id)

    if not obj:
        print(f"Error: {args.model} with ID {args.id} not found.")
        return

    if args.model in ["Teacher", "Student"] and args.name:
        first_name, last_name = args.name.split(" ", 1)
        obj.first_name = first_name
        obj.last_name = last_name

    if args.model == "Student":
        if args.email:
            obj.email = args.email
        if args.group_id:
            obj.group_id = args.group_id

    if args.model in ["Group", "Subject"] and args.name:
        obj.name = args.name

    if args.model == "Subject" and args.teacher_id:
        obj.teacher_id = args.teacher_id

    if args.model == "Grade":
        if args.grade:
            obj.grade = args.grade
        if args.grade_date:
            obj.grade_date = datetime.strptime(args.grade_date, "%Y-%m-%d").date()
        if args.student_id:
            obj.student_id = args.student_id
        if args.subject_id:
            obj.subject_id = args.subject_id

    session.commit()
    print(f"✅ {args.model} with ID {args.id} updated successfully.")


def handle_remove(session: Session, args):
    if not args.id:
        print("Error: --id is required for remove action.")
        return

    model_class = MODELS_MAP[args.model]
    obj = session.get(model_class, args.id)

    if not obj:
        print(f"Error: {args.model} with ID {args.id} not found.")
        return

    session.delete(obj)
    session.commit()
    print(f"✅ {args.model} with ID {args.id} deleted successfully.")


def main():
    args = parse_args()

    with Session(engine) as session:
        try:
            if args.action == "create":
                handle_create(session, args)
            elif args.action == "list":
                handle_list(session, args)
            elif args.action == "update":
                handle_update(session, args)
            elif args.action == "remove":
                handle_remove(session, args)
        except Exception as e:
            session.rollback()
            print(f"DB Error: {e}")


if __name__ == "__main__":
    main()
