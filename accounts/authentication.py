import jwt

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions

from common.utils import get_object_or_none

from .models import User


class TokenAuthentication(BaseAuthentication):
    """Token authentication"""

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY)
        except Exception:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not 'rnd' in payload.keys() or not payload.get('rnd'):
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        user = get_object_or_none(User, pk=payload.get('sub'))

        if not user:
            raise exceptions.AuthenticationFailed(_('User does not exist.'))

        if not user.isActive:
            raise exceptions.AuthenticationFailed(_('User inactive.'))

        if payload.get('rnd') != user.renewed:
            raise exceptions.AuthenticationFailed(_('User password changed.'))

        return (user, key)

    def authenticate_header(self, request):
        return 'Token'


class PasswdTokenAuthentication(TokenAuthentication):
    """Password reset token authentication"""

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY)
        except Exception:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not 'rst' in payload.keys() or not payload.get('rst'):
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        user = get_object_or_none(User, pk=payload.get('sub'))

        if not user:
            raise exceptions.AuthenticationFailed(_('User does not exist.'))

        if not user.isActive:
            raise exceptions.AuthenticationFailed(_('User inactive.'))

        if payload.get('rst') != user.renewed:
            raise exceptions.AuthenticationFailed(_('User password changed.'))

        return (user, key)
