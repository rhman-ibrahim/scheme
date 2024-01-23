#!/bin/bash

# Find all fixtures directories and load JSON files inside them

# Function to load JSON files in a directory
load_fixtures() {
    local directory="$1"
    echo "Loading fixtures in $directory"
    for file in "$directory"/*.json; do
        python manage.py loaddata "$file"
    done
}

# Find all fixtures directories and load JSON files
find . -type d -name 'fixtures' -print0 | while IFS= read -r -d $'\0' dir; do
    load_fixtures "$dir"
done

echo "Finished loading fixtures."
