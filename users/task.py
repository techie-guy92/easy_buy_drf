from celery import shared_task
from django.utils import timezone
from .models import *


# Start the Celery worker
# celery -A core.celery_config worker --loglevel=info

# Start Celery beat
# celery -A core.celery_config beat --loglevel=info

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



