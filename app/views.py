from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse

from rest_framework import status


def not_found(request):
    """Not found view"""
    response = JsonResponse(data={
        'detail': _('Not found.')
    })
    response.status_code = status.HTTP_404_NOT_FOUND
    return response
