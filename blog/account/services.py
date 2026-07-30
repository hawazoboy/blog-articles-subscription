from django.conf import settings
from django.core.mail import send_mail


def send_activation_email(user, activation_url):
    subject = "Activate your account"

    message = f"""
Hello {user.first_name},

Thank you for registering.

Please click the link below to activate your account:

{activation_url}

If you did not create this account, you can safely ignore this email.
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )