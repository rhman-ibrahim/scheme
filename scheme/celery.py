# scheme/celery.py

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheme.settings')

app = Celery('scheme')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every 4 minutes
    'fixing-tokens-uuid-values': {
        'task': 'user.tasks.fixing_tokens_uuid_values',
        'schedule': 45,
    },
}