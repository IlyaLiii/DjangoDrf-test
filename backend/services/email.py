from django.core.mail import send_mail
from django.conf import settings


def send_contact_email_message(subject, message, sender):
    send_mail(
        subject,
        message,
        sender,
        [settings.EMAIL_ADMIN]
    )
