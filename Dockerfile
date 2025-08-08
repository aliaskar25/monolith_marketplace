# syntax=docker/dockerfile:1.6

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Minimal system deps (keep image small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies (cached layer)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Non-root user
RUN useradd -u 1000 -m appuser
USER appuser

# ---------- Dev image ----------
FROM base AS dev
WORKDIR /app
COPY --chown=appuser:appuser docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY --chown=appuser:appuser . /app
ENTRYPOINT ["/entrypoint.sh"]

# ---------- Prod image ----------
FROM base AS prod
WORKDIR /app
COPY --chown=appuser:appuser docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY --chown=appuser:appuser . /app
ENTRYPOINT ["/entrypoint.sh"]
