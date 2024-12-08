FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry \
    && poetry install --no-dev

RUN apt-get update && apt-get install -y \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libxkbcommon0 \
    libasound2 \
    libgbm1 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN playwright install

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "xvfb-run -a uvicorn app.api.endpoints.main:app --host 0.0.0.0 --port 8000"]

