# ============================
# 1) Builder stage
# ============================
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy ONLY dependency definitions first to maximize Docker layer caching
COPY pyproject.toml uv.lock ./

# Mount the uv cache so subsequent builds don't re-download unmodified wheels
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Now copy the rest of the application code
COPY . .

# Second sync to install the project itself (pulls instantly from cache if unchanged)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================
# 2) Runtime stage
# ============================
FROM python:3.14-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create user and directories in a single layer to reduce image size.
# Because this project runs on local SQLite, it is crucial that the appuser
# owns the root /app folder natively so the database can freely generate
# lock/journal files (.sqlite3-journal) during write operations.
RUN useradd -m appuser \
    && mkdir -p /app/static /app/staticfiles \
    && chown -R appuser:appuser /app

# Bring over the isolated virtual environment from the builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Bring over the source code from the host
COPY --chown=appuser:appuser . /app/

USER appuser

# Run collectstatic natively (requires no uv wrapper)
RUN python manage.py collectstatic --noinput

EXPOSE 31247

CMD ["gunicorn", "rota.wsgi:application", "--bind", "0.0.0.0:31247", "--workers", "2", "--worker-class", "gthread", "--threads", "2", "--timeout", "30", "--keep-alive", "2", "--max-requests", "1000", "--max-requests-jitter", "50"]