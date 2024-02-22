#!/bin/bash

# Step 01: Check if a name is provided & create the directories if so.
# Step 02: Initialize a git repo & add base (scheme.api, scheme.ui, scheme.bash).
# Step 03: Manage configuration files & entry point.
# Step 04: Create the Python virtual environment & set NPM prefix.
# Step 05: Install Dependencies.
# Step 06: Create A .gitignore file.
# Step 07: The first commit.
# Step 08: Open the project.

# 01:
if [ -z "$1" ]; then
    echo "Please provide a name for the folder."
    exit 1
else
    mkdir "$1" && cd "$1"
    mkdir submodules modules
    mkdir modules/api modules/ui
fi

# 02:
git init
git submodule add https://github.com/rhman-ibrahim/scheme.bash submodules/scripts
git submodule add https://github.com/rhman-ibrahim/scheme.django submodules/api
git submodule add https://github.com/rhman-ibrahim/scheme.react submodules/ui

# 03:
mv submodules/api/requirements.txt .
mv submodules/ui/package.json .
mv submodules/ui/package-lock.json .
mv submodules/ui/.eslintrc.cjs .
mv submodules/ui/public .
rm submodules/ui/index.html
rm submodules/ui/vite.config.js
rm submodules/ui/jsconfig.json

# 04:
python -m venv venv
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate
npm config set prefix .

# 05:
pip install -r requirements.txt
npm install

# 06:
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

# 07:
git rm --cached -rf scripts/
git rm --cached -rf base/
git add .
git commit -m "Initial commit"

# 08:
code .