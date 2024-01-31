#!/bin/bash

# Step 01: Create a folder named after the $1 value.
# Step 02: Download the release file of $2, unzip then delete the zip file.
# Step 03: Create A Virutal Environment, set both & activate.
# Step 04: Install Dependencies.
# Step 08: Open the project.

# 01:
mkdir $1 && cd $1

# 02:
wget https://github.com/rhman-ibrahim/scheme/releases/download/$2/$2.zip
unzip $2.zip
rm -f $2.zip

# 03:
python -m venv venv
export PYTHONPATH="$PWD/venv/lib/python3.10/site-packages"
source venv/bin/activate
npm config set prefix .

# 04:
pip install -r requirements.txt
npm install

#05: 
code .
