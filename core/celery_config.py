from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('easy_buy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

print("Auto-discovering tasks...")  
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {
#     'check-premium-subscriptions-every-day': {
#         'task': 'users.tasks.check_premium_subscriptions',
#         'schedule': crontab(hour=0, minute=0),  
#     },
# }

app.conf.beat_schedule = {
    'check-premium-subscriptions-every-minute': {
        'task': 'users.tasks.check_premium_subscriptions',
        'schedule': crontab(), 
    },
}