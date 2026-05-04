from celery import shared_task
from users import celery_app
import logging
from django.core.mail import send_mail
from .models import User

logger = logging.getLogger(__name__)


# @shared_task
# def welcome_email_task(user_email, user_name):
#     """
#     Task to send a welcome email to a new user.
#     """
#     # Simulate sending email
#     logger.info(f"Sending welcome email to {user_email}")
#     # Here you would integrate with an email service provider


# @shared_task
# def verification_email_task(user_id, code):
#     try:
#         user = User.objects.get(id=user_id)

#         subject = "Verify Your Account"
#         message = f"Hello {user.get_full_name()},\n\nPlease use the following code to verify your account: {code}\n\nThank you!"
#         from_email = "noreply@yourdomain.com"
#         send_mail(subject, message, from_email, [user.email])
#         logger.info(f"Verification email sent to {user.email}")

#         return True
#     except Exception as e:
#         logger.error(f"Error sending verification email to user {user_id}: {e}")

#         return False


@shared_task
def publish_history_event(event_data):
    try:
        logger.info(f"Publishing history event: {event_data}")
        result = celery_app.send_task(
            "app.tasks.event_task.process_event_background",
            queue="history",
            args=[event_data],
        )
        logger.info(f"History event sent successfully. Task ID: {result}")
    except Exception as e:
        logger.error(f"Error publishing history event: {e}", exc_info=True)
