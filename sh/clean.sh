#!/bin/bash

# Delete cache and migrations files
rm -rf */__pycache__
rm -rf */migrations


# Find all PNG files
png_files=$(find . -wholename "/media/user/tokens/*.png")

# If there are PNG files delete them
if test -n "$png_files"
then rm $png_files
fi

# Delete db.sqlite3 file (Django Database)
if [ -f "db.sqlite3" ]
then rm db.sqlite3
fi

# Delete celerybeat-schedule file
if [ -f "celerybeat-schedule" ]
then rm celerybeat-schedule
fi

# Delete dump.rdb (redis database) file
if [ -f "dump.rdb" ]
then rm dump.rdb
fi