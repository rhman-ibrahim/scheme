#!/bin/bash

# Step 01: Check if a name is provided & create the directories if so.
# Step 02: Initialize a git repo & add base (sch-py, sch-js, sch-sh & sch-cf).
# Step 03: Delete configuration files and entry point from sch-py & sch-js.
# Step 04: Create A .gitignore file.
# Step 05: Create A Virutal Environment, set both & activate.
# Step 06: Install Dependencies.
# Step 07: The first commit.
# Step 08: Open the project.

# 01:
if [ -z "$1" ]; then
    echo "Please provide a name for the folder."
    exit 1
else
    mkdir "$1" && cd "$1"
    mkdir base modules
    mkdir modules/django modules/react
fi

# 02:
git init
git submodule add https://github.com/rhman-ibrahim/scheme.django base/django
git submodule add https://github.com/rhman-ibrahim/scheme.react base/react
git submodule add https://github.com/rhman-ibrahim/scheme.bash scripts
git submodule add https://github.com/rhman-ibrahim/scheme.config configs

# 03:
mv configs/* .
mv base/django/requirements.txt .
mv base/react/package.json .
mv base/react/package-lock.json .
mv base/react/.eslintrc.cjs .
mv base/react/public .
rm base/react/index.html
rm base/react/vite.config.js
rm base/react/jsconfig.json
rm -rf configs

# 04:
echo "\
db.sqlite3
**/migrations/
**/__pycache__/
base/
scripts/
logs/
venv/
node_modules/
" >> .gitignore

# 05:
python -m venv venv
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate
npm config set prefix .

# 06:
pip install -r requirements.txt
npm install

# 07:
git submodule deinit -f configs
git rm --cached -rf scripts/
git rm --cached -rf base/
git rm --cached -rf configs/
git add .
git commit -m "Initial commit"

# 08:
code .