FROM python:3.11-alpine as build
WORKDIR /app
RUN apk add bash
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
RUN touch cron.log

FROM build as dev
WORKDIR /app
CMD crond & env >> /etc/environment && python manage.py runserver 0.0.0.0:8000

FROM build as prod
WORKDIR /app
COPY aws_management/ ./aws_management
COPY app/ ./app
COPY manage.py ./
RUN python manage.py collectstatic --noinput
ENV DEBUG=false
ENV NUM_WORKERS=3
ENV TIMEOUT=120
CMD crond & env >> /etc/environment && python manage.py migrate --noinput && gunicorn aws_management.wsgi --log-level debug --timeout $TIMEOUT --bind 0.0.0.0:8000
