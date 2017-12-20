import os

from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from app.celery import app

from .auth import passwd_token


@app.task
def send_signup_mail(code, email):
    """Send sign up mail"""
    html = render_to_string('accounts/sign_up_code_mail.html', {
        'code': code
    })

    msg = EmailMessage(
        subject=_('Sign up code'),
        body=html,
        to=[email]
    )
    msg.content_subtype = 'html'
    return msg.send(fail_silently=True)


@app.task
def send_passwd_reset_mail(token, username, email):
    """Send passwd reset mail"""
    html = render_to_string('accounts/passwd_reset_mail.html', {
        'username': username,
        'url': os.path.join(settings.PASSWD_RESET_URL, token)
    })

    msg = EmailMessage(
        subject=_('Password reset'),
        body=html,
        to=[email]
    )
    msg.content_subtype = 'html'
    return msg.send(fail_silently=True)
