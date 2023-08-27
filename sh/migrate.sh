#!/bin/bash

# Make migrations
python3 manage.py makemigrations user
python3 manage.py makemigrations team
python3 manage.py makemigrations mate
python3 manage.py makemigrations ping
python3 manage.py makemigrations note
python3 manage.py makemigrations dapi

# Migrate
python3 manage.py migrate