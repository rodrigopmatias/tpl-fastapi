#!/bin/bash

if [ "{{ cookiecutter.database_support }}" != "sqlite" ]; then
  echo "poetry install -E {{ cookiecutter.database_support }}"
  poetry install -E {{ cookiecutter.database_support }}
else
  echo "poetry install"
  poetry install
fi

git init
poetry run pre-commit install
poetry run pre-commit autoupdate
git add .
poetry run pre-commit run -av 
git commit -am "start of project"

openssl rand -base64 -out pub.key 64
