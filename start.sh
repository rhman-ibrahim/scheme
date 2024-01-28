#!/bin/bash

# Step 01: Check if a name is provided & create the directories if so.
# Step 02: Initialize a git repo & add base (scheme, scheme-django & scheme-react).
# Step 03: Create A .gitignore file.
# Step 04: Create A Virutal Environment, set both & activate.
# Step 05: Install Dependencies.
# Step 06: The first commit.

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
git submodule add https://github.com/rhman-ibrahim/scheme-django base/py
git submodule add https://github.com/rhman-ibrahim/scheme-react base/js
git submodule add https://github.com/rhman-ibrahim/scheme scripts
git rm --cached -r base/
git rm --cached -r scripts/

# 03:
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

# 04:
python -m venv venv

# 04: set PYTHONPATH & activate
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate

# 04: set config
npm config set prefix .

# 05: PY
mv base/py/requirements.txt .
pip install -r requirements.txt

# 05: JS
mv base/js/public .
mv base/js/index.html .
mv base/js/jsconfig.json .
mv base/js/package.json .
mv base/js/package-lock.json .
mv base/js/vite.config.js .
mv base/js/.eslintrc.cjs .
npm install

# 06:
git add .
git commit -m "Initial commit"