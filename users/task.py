from celery import shared_task
from time import sleep
from django.utils import timezone
from datetime import timedelta
from .models import *


# Start the Celery worker
# celery -A easy_buy worker --loglevel=info

# Start Celery beat
# celery -A easy_buy beat --loglevel=info


#==================================== UpdateSubscription Model ==========================================

@shared_task
def check_premium_subscriptions():
    now = timezone.now()
    expired_subscriptions = PremiumSubscription.objects.filter(end_date__lt=now)

    for subscription in expired_subscriptions:
        user = subscription.user
        user.is_premium = False
        user.save()
        subscription.delete()  # delete the expired subscription

    print(f"Checked premium subscriptions at {now}")

    
#========================================================================================================



