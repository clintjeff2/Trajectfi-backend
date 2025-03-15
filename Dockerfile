FROM python:3.12-slim-bullseye

WORKDIR /home/trajectfi/src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && apt-get install -y \
    libgirepository1.0-dev \
    gcc \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    gir1.2-gtk-3.0 \
	libgmp3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache \
	pip install -U poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

COPY . .

RUN poetry install

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]