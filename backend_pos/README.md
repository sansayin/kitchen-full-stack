# Prepare environment
In case you don't have kafka and Redis running
Under infra/kafka and infra/redis

- `docker-compose -f up`

# In project folder(manage.py)
## Terminal #1 Run Celery
- celery -A backend_pos.celery worker -l INFO
## Terminal #2 Run Djando
- ./manage.py runserver

# Browser Open
- http://localhost:8080
assume the front end already running, the home page will lead you...
