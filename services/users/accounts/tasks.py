from celery import shared_task
import logging
from django.core.mail import send_mail
from .models import User

logger = logging.getLogger(__name__)


@shared_task
def welcome_email_task(user_email, user_name):
    """
    Task to send a welcome email to a new user.
    """
    # Simulate sending email
    logger.info(f"Sending welcome email to {user_email}")
    # Here you would integrate with an email service provider


@shared_task
def verification_email_task(user_id, code):
    try:
        user = User.objects.get(id=user_id)
    
        subject = "Verify Your Account"
        message = f"Hello {user.get_full_name()},\n\nPlease use the following code to verify your account: {code}\n\nThank you!"
        from_email = "noreply@yourdomain.com"
        send_mail(subject, message, from_email, [user.email])
        logger.info(f"Verification email sent to {user.email}")

        return True
    except Exception as e:
        logger.error(f"Error sending verification email to user {user_id}: {e}")

        return False
