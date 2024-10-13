#!/bin/bash

poetry install -E sqlite

git init
poetry run pre-commit install
poetry run pre-commit autoupdate
git add .
poetry run pre-commit run -av 
git commit -am "start of project"
