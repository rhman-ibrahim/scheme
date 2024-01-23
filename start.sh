#!/bin/bash

# Step 01: Check if a name is provided as an argument.
# Step 02: Create a folder with this name.
# Step 03: Inside this folder, create 3 folders: [submodules, modules].
# Step 04: Initialize a git repo.
# Step 05: Use git add module twice to add scheme-django & scheme-react.
# Step 06: Create A .gitignore file & Add subsubmodules to it.
# Step 07: Create A Virutal Environment.
# Step 08: Activate The Virtual Enviroment.
# Step 09: Install Dependencies.
# Step 10: The first commit.
# Step 11: Display 'End of Script.' Message.

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
echo "/submodules/dj" >> .gitignore
echo "/submodules/re" >> .gitignore

# 07:
python -m venv venv

# 08:Set PYTHONPATH after activation.
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate

# 09:
pip install -r submodules/dj/requirements.txt

# 10:
git add .
git commit -m "Initial commit with subsubmodules (added to the ignore file)."

# 11:
echo "End Of Script."