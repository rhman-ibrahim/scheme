#!/bin/bash

# Make migrations
python3 manage.py makemigrations user
python3 manage.py makemigrations mate
python3 manage.py makemigrations team
python3 manage.py makemigrations blog
python3 manage.py makemigrations ping
python3 manage.py makemigrations dapi

# Migrate
python3 manage.py migrate

# Load fixtures
python3 manage.py loaddata user/fixtures/users.json
python3 manage.py loaddata mate/fixtures/mates.json