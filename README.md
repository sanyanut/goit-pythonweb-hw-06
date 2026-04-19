# goit-pythonweb-hw-06

### Install Dependencies
poetry install


### Create .env or just copy from .env.example
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=


### Start the Database
docker-compose up -d


### Apply Migrations
poetry run alembic upgrade head


### CLI Usage
poetry run python main.py --action <action> --model <model> [additional arguments]


### Creating Records (create)
#### Create a group
poetry run python main.py -a create -m Group -n "AD-101"

#### Create a teacher
poetry run python main.py -a create -m Teacher -n "Boris Johnson"

#### Create a student (group_id is required)
poetry run python main.py -a create -m Student -n "Student Studento" --group_id 1 --email "taras@mail.com"

#### Create a subject (teacher_id is required)
poetry run python main.py -a create -m Subject -n "English" --teacher_id 1

#### Add a grade (student_id and subject_id are required)
poetry run python main.py -a create -m Grade --grade 5 --student_id 1 --subject_id 1 --grade_date "2026-04-19"


### Reading records (list)
#### Show all teachers
poetry run python main.py -a list -m Teacher

#### Show all students
poetry run python main.py -a list -m Student


### Updating Records(update)
#### Change a teacher's name (ID 1)
poetry run python main.py -a update -m Teacher --id 1 -n "Test Tessst"

#### Transfer a student (ID 2) to another group (e.g., ID 3)
poetry run python main.py -a update -m Student --id 2 --group_id 3


### Delete Records (remove)
#### Delete a teacher with ID 3
poetry run python main.py -a remove -m Teacher --id 3