#!/bin/bash

# 01: Navigate to 'modules/dj'.
# 02: Create a new application using 'manage.py'.
# 03: Back to the root.
# 04: Create a soft link for the new app.

cd ../modules/py
python ../../base/py/manage.py startapp "$1"
cd ../../
ln -s "$PWD/modules/py/$1" "$PWD/base/py/apps/$1"