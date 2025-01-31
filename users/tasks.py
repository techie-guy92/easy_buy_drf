from celery import shared_task
from django.utils import timezone
from .models import *


# Start the Celery worker
# celery -A core.celery_config worker --pool=solo --loglevel=info


# Start Celery beat
# celery -A core.celery_config beat --loglevel=info

#==================================== UpdateSubscription Model ==========================================

@shared_task
def check_premium_subscriptions():
    now = timezone.now()
    expired_subscriptions = PremiumSubscription.objects.filter(end_date__lt=now)

    print(f"Expired subscriptions: {expired_subscriptions}")
    
    for subscription in expired_subscriptions:
        user = subscription.user
        user.is_premium = False
        user.save()
        print(f"Updated user: {user.username} is_premium: {user.is_premium}")
        subscription.delete() 

    print(f"Checked premium subscriptions at {now}")


#========================================================================================================



