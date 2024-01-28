#!/bin/bash

# 01: Navigate to the root.
# 02: Define the source & target paths.
# 03: Iterate through each folder in the source path.
    # A: Check if the item is a directory.
    # B: Check if the symbolic link exists in the target path.
    # C: Create symbolic link if not created.
    # D: Print message.


cd ../
source_path="$PWD/modules/py"
target_path="$PWD/base/py/apps"

for folder in "$source_path"/*; do
    folder_name=$(basename "$folder")
    if [ -d "$folder" ]; then
        if [ ! -L "$target_path/$folder_name" ]; then
            ln -s "$source_path/$folder_name" "$target_path/$folder_name"
            echo "Created symbolic link for folder: $folder_name"
        fi
    fi
done

