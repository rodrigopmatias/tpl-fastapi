FROM python:3.12-slim

ARG POETRY_EXTRA_ARGS= \
  GITHUB_AUTHORIZATION=

WORKDIR /app
COPY . .

# hadolint ignore=DL3008,DL3009,DL3013
RUN apt-get update && \
  apt-get install --assume-yes --no-install-recommends git && \
  apt-get clean && \
  rm -fr /var/lib/apt/lists/* && \
  pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir poetry && \
  poetry config virtualenvs.create false && \
  useradd -m -s /bin/bash appuser && \
  git config --global url."https://oauth:${GITHUB_AUTHORIZATION}@github.com".insteadOf https://github.com && \
  poetry install ${POETRY_EXTRA_ARGS} --without=dev && \
  rm -f ~/.gitconfig && \
  apt-get remove git --assume-yes --auto-remove --purge  

EXPOSE 8000/tcp

USER appuser
CMD ["uvicorn", "--factory", "{{ cookiecutter.project_module }}:create_app", "--host", "0", "--port", "8000"]
