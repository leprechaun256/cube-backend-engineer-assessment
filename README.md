# cube-backend-engineer-assessment

To get things started

# Requirements
Python (2.7, 3.4, 3.5, 3.6, 3.7)
Django (1.9, 1.10, 1.11, 2.0.7)

# Init
1. Clone the repository
2. cd assessment

# DB
3. docker run --rm -P -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD="postgres" --name pg postgres:alpine

# Server
4. pip install -r requirements.txt
5. ./manage.py makemigrations
6. ./manage.py migrate
7. ./manage.py dbr
8. ./manage.py runserver

# Output
9. Open localhost:8000/assessment/business-rule on the browser

Setup rules as per the requirement.
