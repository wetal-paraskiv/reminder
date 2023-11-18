# reminder
python Django framework 'reminder' application

1. create local environment & activate it (it's for installing all requirements locally in the project only, not globally)

mkdir project_name
cd project_name
python -m venv envName
envName\scripts\activate

2. clone the project (git clone https://github.com/wetal-paraskiv/reminder.git)

3. install all requirements (pip install -r requirements.txt)

4. cd reminder_django

5. create .env [file content: SECRET_KEY = '$90rf8*mx22p7lq84m)fx+q26j$p7$1$%6%rtd6&q@(ul%owg!']

4. create initial db tables (python manage.py migrate)

5. python manage.py runserver