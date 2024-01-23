#!/bin/bash

# Make migrations
python3 manage.py makemigrations user

# Migrate
python3 manage.py migrate