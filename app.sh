#!/bin/bash


# 01: Navigate to modules/dj
cd ../modules/dj

# 02: Create a new application using 'manage.py'
python manage.py startapp "$1"

# 03: Back to the root
cd ../../

# 04: Create a soft link
ln -s "$PWD/modules/dj/$1" "$PWD/submodules/dj/apps/$1"