from time import time

import jwt

from django.conf import settings
from django.contrib.auth.hashers import check_password

from common.utils import get_object_or_none

from .models import User


def authenticate(username, password, model=User, instance=None):
    """Authenticate user"""
    user = instance or get_object_or_none(model, username=username)
    if user and not check_password(password, user.password):
        user = None
    return user


def auth_token(user):
    """Generate authentication token"""
    now = int(time())
    expire = now + settings.AUTH_TOKEN_EXPIRE

    return jwt.encode({
        'sub': user.id,
        'rnd': user.renewed,
        'iat': now,
        'exp': expire
    }, settings.SECRET_KEY).decode('utf-8')


def passwd_token(user):
    """Generate password reset token"""
    now = int(time())
    expire = now + settings.PASSWD_RESET_TOKEN_EXPIRE

    return jwt.encode({
        'sub': user.id,
        'rst': user.renewed,
        'iat': now,
        'exp': expire
    }, settings.SECRET_KEY).decode('utf-8')
