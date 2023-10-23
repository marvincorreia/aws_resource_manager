FROM python:3.11 as build
WORKDIR /app
RUN apt-get update
RUN apt-get install cron -y
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

FROM build as dev
WORKDIR /app
CMD service cron start && python manage.py runserver 0.0.0.0:8000

FROM build as prod
WORKDIR /app
COPY . .
# RUN python manage.py collectstatic --noinput
CMD service cron start && python manage.py collectstatic --noinput 
# && python manage.py migrate --noinput && gunicorn aws_management.wsgi --bind 0.0.0.0:8000
