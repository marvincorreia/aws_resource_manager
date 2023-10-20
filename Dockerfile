FROM python:3.11

WORKDIR /app
RUN apt-get update
RUN apt-get install cron -y
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
CMD service cron start && python manage.py runscript app.cron.config && python manage.py runserver 0.0.0.0:8000
