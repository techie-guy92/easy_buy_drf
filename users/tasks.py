from celery import shared_task
from logging import getLogger
from django.utils import timezone
import logging
from .models import *


# Start the Celery worker
# on Windows: celery -A core.celery_config worker --pool=solo --loglevel=info
# on Linux:   celery -A core.celery_config worker --loglevel=info
# on Linux:   celery -A core.celery_config worker --pool=solo --loglevel=info -B


# Start Celery beat
# celery -A core.celery_config beat --loglevel=info

#==================================== UpdateSubscription Model ==========================================

logger = logging.getLogger("celery")
logger.setLevel(logging.DEBUG)


@shared_task
def check_premium_subscriptions():
    try:
        now = timezone.now()
        logger.debug(f"Checking for expired subscriptions at {now}")
        expired_subscriptions = PremiumSubscription.objects.filter(end_date__lt=now)
        logger.info(f"Expired subscriptions: {expired_subscriptions}")

        for subscription in expired_subscriptions:
            logger.debug(f"Processing subscription: {subscription}")
            user = subscription.user
            user.is_premium = False
            user.save()
            logger.info(f"Updated user: {user.username} is_premium: {user.is_premium}")
            subscription.delete()
            logger.info(f"Deleted subscription: {subscription}")
        logger.info(f"Checked premium subscriptions at {now}")
    except Exception as e:
        logger.error(f"Error in check_premium_subscriptions: {e}")


#========================================================================================================



