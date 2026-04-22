FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project --no-dev --locked

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

RUN uv sync --no-dev --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
