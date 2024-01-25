#!/bin/bash

# Define root path.
cd ../

# Define the source & target paths.
source_path="$PWD/modules/dj"
target_path="$PWD/submodules/dj/apps"

# Iterate through each folder in the source path
for folder in "$source_path"/*; do
    # Extract folder name
    folder_name=$(basename "$folder")

    # Check if the item is a directory
    if [ -d "$folder" ]; then
        # Check if the symbolic link exists in the target path
        if [ ! -L "$target_path/$folder_name" ]; then
            # Create symbolic link
            ln -s "$source_path/$folder_name" "$target_path/$folder_name"
            echo "Created symbolic link for folder: $folder_name"
        fi
    fi
done

# echo "Symbolic link check and creation completed."
