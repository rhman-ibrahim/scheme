#!/bin/bash

# Export variables
export DJANGO_SETTINGS_MODULE=scheme.settings

# Run Django
gnome-terminal --tab --title "Django" -- bash -c "python manage.py runserver 0.0.0.0:8000"

# Notes
# - To run in a new window:
# gnome-terminal --window --working-directory "$PWD" --title "<title>" -- bash -c "<command>"
# - To run in a new tab:
# gnome-terminal --tab --title "<title>" -- bash -c "<command>"