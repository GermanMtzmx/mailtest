from django.test import TestCase

from rest_framework import status

from .utils import unique_id, to_object
from .serializers import RequestSerializer, ResponseSerializer


class UniqueIdTestCase(TestCase):
    """Unique id test case"""

    def test_a_unique_id_length(self):
        uid = unique_id()
        self.assertEqual(len(uid), 22)


class ToObjectTestCase(TestCase):
    """To object test case"""

    def test_a_dict_to_object(self):
        obj = to_object({'pi': 3.14})
        self.assertTrue(hasattr(obj, 'pi'))


class RequestSerializerTestCase(TestCase):
    """Request serializer test case"""

    def test_a_valid_request(self):
        request = RequestSerializer(data={
            'headers': [
                {
                    'key': 'Content-Type',
                    'value': 'application/json'
                }
            ],
            'body': {
                'action': 'GET',
                'payload': {
                    'id': 25
                }
            }
        })

        self.assertTrue(request.is_valid())


class ResponseSerializerTestCase(TestCase):
    """Response serializer test case"""

    def test_a_valid_response(self):
        response = ResponseSerializer(data={
            'headers': [
                {
                    'key': 'Content-Type',
                    'value': 'application/json'
                }
            ],
            'body': {
                'action': 'RESPONSE',
                'payload': {}
            },
            'status': status.HTTP_200_OK
        })

        self.assertTrue(response.is_valid())
