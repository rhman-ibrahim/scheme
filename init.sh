# Kill Redis port PID
if sudo lsof -i :6379
then sudo lsof -t -i :6379 | sudo xargs kill
fi

# 1 - Run Redis
gnome-terminal --window --working-directory "$PWD" --title "Redis" -- bash -c "redis-server"

# 2 - Run Django
gnome-terminal --window --working-directory "$PWD" --title "Django" -- bash -c "python manage.py runserver 0.0.0.0:8000"

# 3 - Run Celery Worker
gnome-terminal --window --working-directory "$PWD" --title "Celery/Worker" -- bash -c "celery -A scheme worker -l info"

# 4 - Run Celery Beat
gnome-terminal --window --working-directory "$PWD" --title "Celery/Beat" -- bash -c "celery -A scheme beat -l info"