from celery import shared_task
from logging import getLogger
from django.utils import timezone
from .models import *


# Start the Celery worker
# on Windows: celery -A core.celery_config worker --pool=solo --loglevel=info
# on Linux:   celery -A core.celery_config worker --loglevel=info
# on Linux:   celery -A core.celery_config worker --pool=solo --loglevel=info -B


# Start Celery beat
# celery -A core.celery_config beat --loglevel=info

#==================================== UpdateSubscription Model ==========================================

logger = getLogger("celery")


@shared_task
def check_premium_subscriptions():
    now = timezone.now()
    expired_subscriptions = PremiumSubscription.objects.filter(end_date__lt=now)
    logger.debug(f"Expired subscriptions: {expired_subscriptions}")
    
    for subscription in expired_subscriptions:
        user = subscription.user
        user.is_premium = False
        user.save()
        logger.debug(f"Updated user: {user.username} is_premium: {user.is_premium}")
        subscription.delete() 

    logger.info(f"Checked premium subscriptions at {now}")


#========================================================================================================



