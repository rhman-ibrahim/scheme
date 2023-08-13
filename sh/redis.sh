#!/bin/bash

# Kill Redis PID
if sudo lsof -i :6379
then sudo lsof -t -i :6379 | sudo xargs kill
fi

# Restart Redis service
sudo systemctl restart redis.service

# Run Redis
gnome-terminal --tab --title "Redis" -- bash -c "redis-server"