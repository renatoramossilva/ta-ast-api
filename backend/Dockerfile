FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry uvicorn

WORKDIR /app/backend

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.api.endpoints.main:app --host 0.0.0.0 --port 8000"]
