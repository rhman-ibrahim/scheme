#!/bin/bash

# Step 01: Check if a name is provided as an argument.
# Step 02: Create a folder with this name.
# Step 03: Inside this folder, create 3 folders: [submodules, modules].
# Step 04: Initialize a git repo.
# Step 05: Use git add module to add scheme, scheme-django & scheme-react.
# Step 06: Create a soft link for manage.py where needed.
# Step 07: Create A .gitignore file & Add subsubmodules to it.
# Step 08: Create A Virutal Environment.
# Step 09: Activate The Virtual Enviroment.
# Step 10: Install Dependencies.
# Step 11: The first commit.
# Step 12: Display 'End of Script.' Message.

# 01:
if [ -z "$1" ]; then
    echo "Please provide a name for the folder."
    exit 1
fi

# 02:
mkdir "$1" && cd "$1" || exit

# 03: Inside modules create [dj, re].
mkdir submodules modules modules/dj modules/re

# 04:
git init

# 05:
git submodule add https://github.com/rhman-ibrahim/scheme-django submodules/dj
git submodule add https://github.com/rhman-ibrahim/scheme-react submodules/re
git submodule add https://github.com/rhman-ibrahim/scheme scripts

# 06:
ln -s "$PWD/submodules/dj/manage.py" "$PWD/scripts/manage.py"

# 07:
ignore_list="\
**/migrations/
**/__pycache__/
/submodules/dj/
/submodules/re/
/scripts/
/logs/
/db.sqlite3
"
echo "$ignore_list" >> .gitignore

# 08:
python -m venv venv

# 09:Set PYTHONPATH after activation.
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate

# 10:
pip install -r submodules/dj/requirements.txt

# 11:
git add .
git commit -m "Initial commit with subsubmodules (added to the ignore file)."

# 12:
echo "End Of Script."