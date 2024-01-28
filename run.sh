#!/bin/bash

manage_utility_path="../base/py/manage.py"

if [ -z "$1" ]; then
    echo "'t' for a new tab."
    echo "'w' for a new window."
    exit 1
fi

if [ "$1" = "t" ]; then
    gnome-terminal --tab --title "Django" -- bash -c "python $manage_utility_path runserver 0.0.0.0:8000"
    gnome-terminal --tab --title "React" -- bash -c "npm run dev"
elif [ "$1" = "w" ]; then
    gnome-terminal --window --title "Django" -- bash -c "python $manage_utility_path runserver 0.0.0.0:8000"
    gnome-terminal --window --title "React" -- bash -c "npm run dev"
else
    echo "Invalid argument. Please provide 't' for tab or 'w' for window."
    exit 1
fi