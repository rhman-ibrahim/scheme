#!/bin/bash

# Delete cache tokens, files and migrations
rm /media/tokens/*.png
rm -rf */__pycache__
rm -rf */migrations

# Delete db.sqlite3 file
if [ -f "db.sqlite3" ]
then rm db.sqlite3
fi

# Delete celerybeat-schedule file
if [ -f "celerybeat-schedule" ]
then rm celerybeat-schedule
fi

# Delete dump.rdb (redis) file
if [ -f "dump.rdb" ]
then rm dump.rdb
fi

# Restart Redis service
sudo systemctl restart redis.service

# Make migrations
python3 manage.py makemigrations user
python3 manage.py makemigrations circles
python3 manage.py makemigrations signals
python3 manage.py makemigrations spaces
python3 manage.py makemigrations tasks

# Migrate
python3 manage.py migrate

# Load fixtures
python3 manage.py loaddata user/fixtures/users.json

if sudo lsof -i :6379
then sudo lsof -t -i :6379 | sudo xargs kill
fi

# 1 - Run Redis
gnome-terminal --window --working-directory "$PWD" --title "Redis" -- bash -c "redis-server"

# 2 - Run Django
gnome-terminal --window --working-directory "$PWD" --title "Django" -- bash -c "python manage.py runserver 0.0.0.0:8000"

# 3 - Run Celery Worker
gnome-terminal --window --working-directory "$PWD" --title "Celery/Worker" -- bash -c "celery -A scheme worker -l info"

# 4 - Run Celery Beat
gnome-terminal --window --working-directory "$PWD" --title "Celery/Beat" -- bash -c "celery -A scheme beat -l info"