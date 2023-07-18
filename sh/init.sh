#!/bin/bash

# Export variables
export DJANGO_SETTINGS_MODULE=scheme.settings

# Kill Redis port PID
if sudo lsof -i :6379
then sudo lsof -t -i :6379 | sudo xargs kill
fi

# Restart Redis service
sudo systemctl restart redis.service
