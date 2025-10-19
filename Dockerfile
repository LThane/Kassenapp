# syntax=docker/dockerfile:1

# --- Base image ---
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    REFLEX_ENV=prod

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node (needed by Reflex for building frontend)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifests first for better layer caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app source
COPY . .

# Expose the port the app listens on
EXPOSE 3000

# Healthcheck (basic)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:3000/ || exit 1

# Start the Reflex app (backend server)
CMD ["reflex", "run"]