#!/bin/bash

# To run in a new window:
# gnome-terminal --window --working-directory "$PWD" --title "<title>" -- bash -c "<command>"

# To run in a new tab:
# gnome-terminal --tab --title "<title>" -- bash -c "<command>"

# 1 - Run Redis
gnome-terminal --tab --title "Redis" -- bash -c "redis-server"

# 2 - Run Django
gnome-terminal --tab --title "Django" -- bash -c "python manage.py runserver 0.0.0.0:8000"

# 3 - Run Celery Worker
gnome-terminal --tab --title "Celery/Worker" -- bash -c "celery -A scheme worker -l info"

# 4 - Run Celery Beat
gnome-terminal --tab --title "Celery/Beat" -- bash -c "celery -A scheme beat -l info"

# 5 - Open VSCODE
code .