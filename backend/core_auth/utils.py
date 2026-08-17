from django.tasks import task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@task()
def send_otp_email(email: str, code: str):
    """
    Runs outside the request-response cycle using Django 6.0's task framework.
    """
    try:
        send_mail(
            subject="Your Secure Login Code",
            message=f"Your one-time password is: {code}\n\nThis code expires in 5 minutes.",
            from_email=None,  # Falls back to DEFAULT_FROM_EMAIL in settings
            recipient_list=[email],
        )
    except Exception as e:
        logger.error(f"Failed to send OTP to {email}: {str(e)}")
        # The task framework will capture this error in the TaskResult
        raise e