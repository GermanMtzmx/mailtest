import base64
import uuid

from datetime import datetime

import requests

from django.conf import settings
from django.core.mail import EmailMessage


def get_object_or_none(model, *args, **kwargs):
    """Get object or none"""
    try:
        obj = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        obj = None
    return obj


def unique_id():
    """Generate unique id"""
    return base64.urlsafe_b64encode(uuid.uuid4(
        ).bytes).decode('utf-8').replace('==', '')


def to_object(data):
    """Data to object"""

    iterable = (list, tuple, set)
    if isinstance(data, iterable):
        return [to_object(i) for i in data]

    if not isinstance(data, dict):
        return data

    global Obj

    class Obj: pass

    obj = Obj()
    for k, v in data.items():
        setattr(obj, k, to_object(v))
    return obj


def send_notification(title='', body='', icon='', data={}, to=[]):
    """Send firebase push notification"""
    if not to: return

    return requests.post(settings.FCM_URL, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Key=%s' % settings.FCM_TOKEN
    }, json={
        'registration_ids': to,
        'notification': { # Max. 2KB.
            'title': title,
            'body': body,
            'icon': icon or settings.FCM_DEFAULT_ICON
        },
        'data': data # Max. 4KB.
    })


def send_email(subject, htmlContent, to, cc=None):
    """send html email"""
    email = EmailMessage(
        subject=subject,
        body=htmlContent,
        to=[to],
        cc=['xti.store.mexico.1@gmail.com']
    )

    email.content_subtype = 'html'
    email.send(fail_silently=False)
