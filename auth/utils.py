from random import randint

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from auth.models import VerificationCode
from core.exceptions import EmailNotFound


def generate_verification_code():
    return randint(100000, 999999)


def send_mail(
    email, subject, context, html_file, from_email='test@test.com'
):
    html_message = render_to_string(html_file, context)
    if settings.MAIL_ENABLED and settings.EMAIL_VERIFY:
        if email:

            email = EmailMessage(
                subject=subject,
                body=html_message,
                to=[email],
                from_email=from_email
            )
            email.content_subtype = 'html'
            email.send(fail_silently=True)
        else:
            raise EmailNotFound


def send_code_for_verify(email):
    verification_code = generate_verification_code()
    VerificationCode.objects.create(email=email, code=verification_code)
    context = {
        'code': verification_code,
    }
    html_file = f'auth/email_verify.html'

    send_mail(
        email=email,
        subject='Please verify your account',
        context=context,
        html_file=html_file
    )
