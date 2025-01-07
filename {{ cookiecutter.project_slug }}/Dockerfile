FROM python:3.12-slim

ARG POETRY_EXTRA_ARGS=

WORKDIR /app

COPY README.md poetry.lock pyproject.toml /app/

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir poetry && \
  poetry config virtualenvs.create false && \
  useradd -m -s /bin/bash appuser

COPY --chown=appuser:appuser . .
RUN poetry install ${POETRY_EXTRA_ARGS} --without=dev 

EXPOSE 8000/tcp

USER appuser
CMD ["uvicorn", "--factory", "{{ cookiecutter.project_module }}:create_app", "--host", "0", "--port", "8000"]
