# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from logging import getLogger

logger = getLogger("celery")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery('easy_buy')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# app.conf.beat_schedule = {
#     'check-premium-subscriptions-every-minute': {
#         'task': 'users.tasks.check_premium_subscriptions',
#         'schedule': crontab(hour=0, minute=0),
#     },
# }