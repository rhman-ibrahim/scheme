#!/bin/bash

manage_utility_path="../submodules/dj/manage.py"

python $manage_utility_path makemigrations user
python $manage_utility_path migrate