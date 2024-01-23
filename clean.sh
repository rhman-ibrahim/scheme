#!/bin/bash

# Navigate to the root directory of the project (parent of 'scripts' directory)
cd "$(dirname "$(pwd)")" || exit

# Delete all 'migrations' directories
find . -type d -name 'migrations' -exec rm -r {} +

# Delete all '__pycache__' directories
find . -type d -name '__pycache__' -exec rm -r {} +

# Delete 'db.sqlite3' file
find . -type f -name 'db.sqlite3' -exec rm {} +