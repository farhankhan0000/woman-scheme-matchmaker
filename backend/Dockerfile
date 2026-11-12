
# Python base image
FROM python:3.12-slim

# Install the same uv version used by the project setup.
COPY --from=ghcr.io/astral-sh/uv:0.12.13 /uv /uvx /bin/

WORKDIR /app

# Keep the container's environment outside the source bind mount.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONUNBUFFERED=1

# Copy dependency files first for Docker layer caching.
COPY pyproject.toml uv.lock .python-version ./

# Install locked production dependencies.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# Copy backend source code.
COPY . .

# Make the virtual environment executable available.
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

# Development server with automatic reload.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
