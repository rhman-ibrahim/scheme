#!/bin/bash

# Delete cache files
rm -rf scheme/__pycache__
rm -rf scheme/*/__pycache__
rm -rf scheme/base/apps/__pycache__
rm -rf scheme/base/apps/*/__pycache__
rm -rf scheme/base/apps/*/models/__pycache__
rm -rf scheme/base/apps/*/views/__pycache__

# Delete migrations files
rm -rf scheme/base/apps/*/migrations

# Delete db.sqlite3 file (Django Database)
if [ -f "db.sqlite3" ]
    then rm db.sqlite3
fi

# # Delete celerybeat-schedule file
if [ -f "celerybeat-schedule" ]
    then rm celerybeat-schedule
fi

# Delete dump.rdb (redis database) file
if [ -f "dump.rdb" ]
    then rm dump.rdb
fi