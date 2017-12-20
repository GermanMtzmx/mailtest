import pytz

from django.conf import settings
from django.utils import timezone, translation


class TimeZoneMiddleware:
    """Time zone middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.META.get('HTTP_TIME_ZONE', '')

        tzinfo = self.__get_tzinfo(tzname)
        if tzinfo:
            timezone.activate(tzinfo)

        response = self.get_response(request)

        timezone.deactivate()
        return response

    def __get_tzinfo(self, tzname):
        """Get time zone info"""
        try:
            tzinfo = pytz.timezone(tzname)
        except pytz.exceptions.UnknownTimeZoneError:
            tzinfo = None
        return tzinfo


class AdminLocaleMiddleware:
    """Admin locale middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            translation.activate(settings.LANGUAGE_CODE)

        response = self.get_response(request)

        translation.deactivate()
        return response
