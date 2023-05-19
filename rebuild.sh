#!/bin/bash

# Delete databases, Celery files
if [ -f "celerybeat-schedule" ]
then
    rm celerybeat-schedule
fi

if [ -f "db.sqlite3" ]
then
    rm db.sqlite3
fi

if [ -f "dump.rdb" ]
then
    rm dump.rdb
fi

# Delete cache files and migrations
rm -rf */__pycache__
rm -rf */migrations

# Make migrations
python3 manage.py makemigrations user
python3 manage.py makemigrations circles
python3 manage.py makemigrations signals
python3 manage.py makemigrations spaces

# Migrate
python3 manage.py migrate

# Load fixtures
python3 manage.py loaddata user/fixtures/users.json