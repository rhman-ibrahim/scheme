source venv/bin/activate
export DJANGO_SETTINGS_MODULE=scheme.settings

# Kill Redis port PID
if sudo lsof -i :6379
then sudo lsof -t -i :6379 | sudo xargs kill
fi

# 1 - Run Django
gnome-terminal --tab --title "Django" -- bash -c "python manage.py runserver 0.0.0.0:8000"

# 2 - Run Redis
gnome-terminal --tab --title "Redis" -- bash -c "redis-server"

# 3 - Run Celery Worker
gnome-terminal --tab --title "Celery/Worker" -- bash -c "celery -A scheme worker -l info"

# 4 - Run Celery Beat
gnome-terminal --tab --title "Celery/Beat" -- bash -c "celery -A scheme beat -l info"

# 5 - Open VSCODE
code .
