#!/bin/bash

# Run Celery Worker
gnome-terminal --tab --title "Celery/Worker" -- bash -c "celery -A scheme worker -l info"

# Run Celery Beat
gnome-terminal --tab --title "Celery/Beat" -- bash -c "celery -A scheme beat -l info"