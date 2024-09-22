FROM python:3.10.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --with main --no-ansi --no-root

COPY ./alembic.ini ./

COPY ./accommodations.json ./

COPY ./reviews.json ./

COPY ./src ./src
