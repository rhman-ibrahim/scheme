#!/bin/bash

# 01: Navigate to the root directory of the project (parent of 'scripts' directory).
# 02: Find and delete all 'migrations' directories excluding 'venv'.
# 03: Find and delete all '__pycache__' directories excluding 'venv'.
# 04: Find and delete 'db.sqlite3' file.

cd "$(dirname "$(pwd)")" || exit
find . -type d \( -name 'migrations' -o -name 'venv' \) -prune -exec rm -r {} +
find . -type d \( -name '__pycache__' -o -name 'venv' \) -prune -exec rm -r {} +
find . -type f -name 'db.sqlite3' -exec rm {} +