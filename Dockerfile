# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NEUROVISION_ENVIRONMENT=production \
    NEUROVISION_DATA_DIR=/app/data

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --locked --no-dev --no-cache \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin neurovision \
    && mkdir -p /app/data \
    && chown -R neurovision:neurovision /app /opt/venv

USER 10001:10001

CMD ["python", "-c", "from neurovision import __version__; print(f'NeuroVision {__version__} container ready')"]
