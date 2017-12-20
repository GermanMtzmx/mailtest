from time import time

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings


def generate_user_renewed():
    """Generate user renewed"""
    return int(time())


def generate_code():
    """Generate sign up code"""
    return get_random_string(
        length=4, allowed_chars='0123456789')


def generate_code_expired():
    """Generate sign up expired"""
    return timezone.now() + timezone.timedelta(
        seconds=settings.SIGNUP_CODE_EXPIRE)
