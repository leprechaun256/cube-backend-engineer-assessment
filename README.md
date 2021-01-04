# cube-backend-engineer-assessment

To get things started

# Init
1. Clone the repository
2. cd assessment

# DB
3. docker run --rm -P -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD="postgres" --name pg postgres:alpine

# Server
4. ./manage.py makemigrations
5. ./manage.py migrate
6. ./manage.py dbr
7. ./manage.py runserver

# Output
8. Open localhost:8000/assessment/business-rule on the browser
9. Setup rules as per the requirement.
