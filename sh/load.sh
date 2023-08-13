#!/bin/bash

# Load data
python3 manage.py loaddata user/fixtures/users.json
python3 manage.py loaddata mate/fixtures/mates.json
python3 manage.py loaddata team/fixtures/teams.json
# python3 manage.py loaddata blog/fixtures/posts.json