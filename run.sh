#!/bin/bash

manage_utility_path="../submodules/dj/manage.py"

if [ -z "$1" ]; then
    echo "'t' for a new tab."
    echo "'w' for a new window."
    exit 1
fi

if [ "$1" = "t" ]; then
    gnome-terminal --tab --title "Django" -- bash -c "python $manage_utility_path runserver 0.0.0.0:8000"
elif [ "$1" = "w" ]; then
    gnome-terminal --window --working-directory "$PWD" --title "Django" -- bash -c "python $manage_utility_path runserver 0.0.0.0:8000"
else
    echo "Invalid argument. Please provide 't' for tab or 'w' for window."
    exit 1
fi