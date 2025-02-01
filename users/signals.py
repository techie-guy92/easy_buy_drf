from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from logging import getLogger
from .models import *
from utilities import *


#==================================== UpdateSubscription Model ==========================================

logger = getLogger("celery")


@receiver(post_save, sender=Payment)
def update_subscription(sender, instance, **kwargs):
    if instance.payment_status == "completed":
        instance.process_payment()
        logger.info(f"Processed payment for user: {instance.user.username}")

@receiver(post_save, sender=PremiumSubscription)
def check_subscription_expiration(sender, instance, **kwargs):
    logger.debug(f"Signal triggered for subscription: {instance}")
    logger.debug(f"Current time: {timezone.now()}")
    logger.debug(f"Subscription end time: {instance.end_date}")

    if instance.is_expired():
        logger.info(f"Subscription expired: {instance}")
        user = instance.user
        user.is_premium = False
        user.save()
        logger.info(f"Updated user: {user.username} is_premium: {user.is_premium}")
    else:
        logger.info(f"Subscription not expired: {instance.end_date} >= {timezone.now()}")


#========================================================================================================