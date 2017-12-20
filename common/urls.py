from django.urls import include, re_path as path

from .views import (
    FruitAPIView,
    DateTimeAPIView,
    ServeAPIView,
    FCMAPIView,
    MsgAPIView,
)


urlpatterns = [
    path(r'^common/fruits$', FruitAPIView.as_view(), name='fruits'),
    path(r'^common/localtime$', DateTimeAPIView.as_view(), name='localtime'),
    path(r'^common/serve/(?P<path>.*)$', ServeAPIView.as_view(), name='serve'),
    path(r'^common/fcm/send$', FCMAPIView.as_view(), name='fcm-send'),
    path(r'^common/rooms/(?P<room_id>[0-9]+)/msgs$', MsgAPIView.as_view(), name='msg-send'),
]
