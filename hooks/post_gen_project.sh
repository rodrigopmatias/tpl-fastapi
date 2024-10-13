#!/bin/bash

poetry install -E {{ cookiecutter.database_support }}

git init
poetry run pre-commit install
poetry run pre-commit autoupdate
git add .
poetry run pre-commit run -av 
git commit -am "start of project"

openssl rand -base64 -out pub.key 64
