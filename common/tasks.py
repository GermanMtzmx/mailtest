from mailtest.celery import app

from .utils import send_notification


@app.task
def add(a, b):
    """Add"""
    return a + b


@app.task
def send_fcm_notification(*args, **kwargs):
    """Send fcm notification"""
    send_notification(*args, **kwargs)
