FROM python:3.14-slim

# Database type (postgres, mysql, or sqlite)
ARG DATABASE_TYPE=sqlite
ENV UV_SYSTEM_PYTHON=1

RUN apt-get update && \
  apt-get install -y --no-install-recommends git=2.52.0 && \
  rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY app ./app

RUN uv sync --group ${DATABASE_TYPE} --no-dev --frozen

CMD ["uv", "run", "app"]
