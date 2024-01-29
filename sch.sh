#!/bin/bash

# Step 01: Check if a name is provided & create the directories if so.
# Step 02: Initialize a git repo & add base (sch-py, sch-js, sch-sh & scheme-conf).
# Step 03: Delete configuration files and entry point from sch-py & sch-js.
# Step 04: Create A .gitignore file.
# Step 05: Create A Virutal Environment, set both & activate.
# Step 06: Install Dependencies.
# Step 07: The first commit.

# 01:
if [ -z "$1" ]; then
    echo "Please provide a name for the folder."
    exit 1
else
    mkdir "$1" && cd "$1"
    mkdir base modules
    mkdir modules/py modules/js
fi

# 02:
git init
git submodule add https://github.com/rhman-ibrahim/sch-py base/py
git submodule add https://github.com/rhman-ibrahim/sch-js base/js
git submodule add https://github.com/rhman-ibrahim/sch-sh scripts
git submodule add https://github.com/rhman-ibrahim/sch-conf .
git rm --cached -r base/
git rm --cached -r scripts/

# 03:
rm -rf base/js/public
rm base/js/index.html
rm base/py/requirements.txt
rm base/js/package.json
rm base/js/package-lock.json
rm base/js/vite.config.js
rm base/js/.eslintrc.cjs
rm base/js/jsconfig.json

# 04:
ignore_list="\
db.sqlite3
**/migrations/
**/__pycache__/
base/
scripts/
logs/
venv/
node_modules/
"
echo "$ignore_list" >> .gitignore

# 05:
python -m venv venv
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate
npm config set prefix .

# 06:
pip install -r requirements.txt
npm install

# 07:
git add .
git commit -m "Initial commit"
