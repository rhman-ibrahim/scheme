# scheme/celery.py

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheme.settings')

app                    = Celery('scheme')

app.conf.update(
    broker_url         = 'redis://localhost:6379/0',
    result_backend     = 'redis://localhost:6379/0',
    accept_content     = ['json'],
    task_serializer    = 'json',
    result_serializer  = 'json',
    timezone           = 'UTC'
)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every 4 minutes
    'fixing-tokens-uuid-values': {
        'task': 'user.tasks.fixing_tokens_uuid_values',
        'schedule': 45,
    },
    # 'fixing-tokens-uuid-values': {
    #     'task': 'user.tasks.deactivating_guest_user_accounts',
    #     'schedule': 3600,
    # },
}