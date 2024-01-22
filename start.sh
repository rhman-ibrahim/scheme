#!/bin/bash

# Check if a name is provided as an argument
if [ -z "$1" ]; then
    echo "Please provide a name for the folder."
    exit 1
fi

# Step 1: Receive a name
folder_name=$1

# Step 2: Create a folder with this name
mkdir "$folder_name"

# Step 3: Inside this folder, create 3 folders: [modules, dj, re]
cd "$folder_name" || exit

mkdir modules dj re

# Step 4: Use git add module twice to add 2 repos as submodules [modules/dj, modules/re]
git init
git submodule add https://github.com/rhman-ibrahim/scheme-django modules/dj
git submodule add https://github.com/rhman-ibrahim/scheme-react modules/re

# Step 5: Create a .gitignore file and add submodules to it
echo "/modules/dj" >> .gitignore
echo "/modules/re" >> .gitignore

# Commit the changes
git add .
git commit -m "Initial commit with submodules (added to the ignore file)."

# Display success message
echo "Directories and submodules created successfully."
