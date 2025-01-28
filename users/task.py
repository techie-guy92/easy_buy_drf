from celery import shared_task
from time import sleep
from django.utils import timezone
from datetime import timedelta
from .models import *


# celery -A core.celery_config worker --loglevel=info

#==================================== UpdateSubscription Model ==========================================

# @shared_task
# def check_premium_status():
#     now = timezone.now()
#     users = CustomUser.objects.filter(is_premium=True, premium_expiry_date__lt=now)
#     users.update(is_premium=False)
    
    
#========================================================================================================



