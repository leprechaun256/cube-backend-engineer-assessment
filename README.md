# cube-backend-engineer-assessment

To get things started

# Requirements
a. Python (2.7, 3.4, 3.5, 3.6, 3.7)
b. Django (1.9, 1.10, 1.11, 2.0.7)
c. pip
d. Docker
e. Redis

# Init
1. Clone the repository
2. cd assessment

# DB + Redis (in new terminals)
3a. 
docker run --rm -P -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD="postgres" --name pg postgres:alpine

3b. 
wget http://download.redis.io/releases/redis-5.0.5.tar.gz
tar xzf redis-5.0.5.tar.gz
cd redis-5.0.5
make
src/redis-server


# Server
4. pip install -r requirements.txt
5. ./manage.py makemigrations cube django_business_rules
6. ./manage.py migrate
7. ./manage.py dbr
8. ./manage.py runserver

# Output
9. Open localhost:8000/assessment/business-rule on the browser

Setup rules as per the requirement.
