#!/bin/bash

manage_utility_path="../base/py/manage.py"

python $manage_utility_path makemigrations user
python $manage_utility_path migrate