from celery import shared_task
from time import sleep


# celery -A core.celery_config worker --loglevel=info

@shared_task
def add_num(x, y):
    sleep(10)
    return x + y

