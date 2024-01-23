#!/bin/bash

# Navigate to the root directory of the project (parent of 'scripts' directory)
cd "$(dirname "$(pwd)")" || exit

# Delete all 'migrations' directories excluding 'venv'
find . -type d \( -name 'migrations' -o -name 'venv' \) -prune -exec rm -r {} +

# Delete all '__pycache__' directories excluding 'venv'
find . -type d \( -name '__pycache__' -o -name 'venv' \) -prune -exec rm -r {} +

# Delete 'db.sqlite3' file
find . -type f -name 'db.sqlite3' -exec rm {} +