#!/bin/bash

# Function to load JSON files in a directory.
load_fixtures() {
    local directory="$1"
    echo "Loading fixtures in $directory"
    for file in "$directory"/*.json; do
        python ../base/py/manage.py loaddata "$file"
    done
}

# Find all 'fixtures' directories recursively under 'modules' and 'base'.
find ../modules/py ../base/py -type d -name 'fixtures' -print0 | while IFS= read -r -d $'\0' dir; do
    load_fixtures "$dir"
done

echo "Finished loading fixtures."
