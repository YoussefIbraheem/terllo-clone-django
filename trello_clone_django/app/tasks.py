from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def welcome_email_task(user_email, user_name):
    """
    Task to send a welcome email to a new user.
    """
    # Simulate sending email
    logger.info(f"Sending welcome email to {user_email}")
    # Here you would integrate with an email service provider
    print(f"Welcome {user_name}! Your email {user_email} has been registered.")