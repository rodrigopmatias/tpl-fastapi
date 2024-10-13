FROM python:3.12-slim

ARG APP_EXTRA=sqlite 

WORKDIR /app

COPY README.md poetry.lock pyproject.toml /app/

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir poetry && \
  poetry config virtualenvs.create false && \
  poetry install -E "${APP_EXTRA}" && \
  useradd -m -s /bin/bash appuser

COPY --chown=appuser:appuser . .

EXPOSE 8000/tcp

USER appuser
CMD ["uvicorn", "--factory", "fastapi_template:create_app", "--host", "0", "--port", "8000"]
