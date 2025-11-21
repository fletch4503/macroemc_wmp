FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install -e .

COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000