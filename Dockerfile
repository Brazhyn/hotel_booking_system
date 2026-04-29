FROM python:3.11.15

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser . .

CMD alembic upgrade head; python src/main.py