from rest_framework.response import Response as DRFResponse
from rest_framework.status import is_client_error

from . import errors


class Response(DRFResponse):
    """Response"""

    def __init__(self, *args, **kwargs):
        self.__get_error(kwargs)
        super(self.__class__, self).__init__(*args, **kwargs)

    def __get_error(self, kwargs):
        if not is_client_error(kwargs['status']):
            return

        for k, v in kwargs.get('data', {}).items():
            kwargs['data'] = {
                'code': int(v[1]) if len(v) == 2
                    else errors.FORM_ERROR,
                'detail': v[0], 'field': k}
