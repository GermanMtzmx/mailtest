from django.views.static import serve
from django.utils import timezone
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import AllowAny

from common.pagination import PageNumberPagination
from common.utils import to_object

from .serializers import (
    FruitListSerializer, FCMSerializer, MsgSerializer)


class FruitAPIView(APIView):
    """Fruit api view"""

    queryset = [to_object({'name': fruit}) for fruit in [
        'Apple', 'Orange', 'Lemon',
        'Melon', 'Strawberry', 'Grape'
    ]] * 1000000

    serializer_class = FruitListSerializer

    pagination_class = PageNumberPagination

    def get(self, request):
        paginator = self.pagination_class()

        data = paginator.paginate_queryset(
            self.queryset, self.request)

        serializer = self.serializer_class(data, many=True)
        return paginator.get_paginated_response(serializer.data)


class DateTimeAPIView(APIView):
    """Date time api view"""

    def get(self, request):
        """Get local time"""
        return Response(data={
            'localTime': timezone.localtime(
                timezone.now()).isoformat()
        }, status=status.HTTP_200_OK)


class ServeAPIView(APIView):
    """Serve api view"""

    permission_classes = (AllowAny,)

    def get(self, request, path):
        """Get file"""
        return serve(request, path,
            document_root=settings.MEDIA_ROOT)


class FCMAPIView(APIView):
    """FCM api view"""

    serializer_class = FCMSerializer

    def post(self, request):
        """Send push notification"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_200_OK)


class MsgAPIView(APIView):
    """Message api view"""

    serializer_class = MsgSerializer

    def post(self, request, room_id):
        """Send message to group"""
        serializer = self.serializer_class(
            data=request.data, context={'room_id': room_id})
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_200_OK)
