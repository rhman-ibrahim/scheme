#!/bin/bash

mv "../scheme" "../project_name"

old_word="scheme"
new_word="{{ project_name }}"

files="
../manage.py
../project_name/asgi.py
../project_name/wsgi.py
../project_name/settings/base.py
"

for file in $files; do
    echo "Replacing '$old_word' with '$new_word' in $file..."
    sed -i "s/\b$old_word\b/$new_word/g" "$file"
done

echo "Transformed into a package."
