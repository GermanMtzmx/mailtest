from django.utils import timezone
from rest_framework import serializers
from channels import Group

from .utils import to_object
from .tasks import send_fcm_notification


class DateTimeTZField(serializers.DateTimeField):
    """Date time tz field"""

    def to_internal_value(self, data):
        return super(DateTimeTZField, self
            ).to_internal_value(timezone.localtime(data))

    def to_representation(self, value):
        return super(DateTimeTZField, self
            ).to_representation(timezone.localtime(value))


class FruitListSerializer(serializers.Serializer):
    """Fruit list serializer"""

    name = serializers.CharField(max_length=50)


class FCMSerializer(serializers.Serializer):
    """FCM serializer"""

    title = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=150)

    to = serializers.CharField(max_length=200)

    def create(self, validated_data):
        send_fcm_notification.delay(
            title=validated_data['title'],
            body=validated_data['body'],
            to=[validated_data['to']]
        )
        return to_object(validated_data)


class MsgSerializer(serializers.Serializer):
    """Message serializer"""

    content = serializers.CharField(max_length=250)

    def create(self, validated_data):
        room_id = self.context['room_id']
        content = validated_data['content']

        Group('room-%s' % room_id).send({'text': content})
        return to_object(validated_data)


class HeaderSerializer(serializers.Serializer):
    """Header serializer"""

    key = serializers.CharField(max_length=50)
    value = serializers.CharField(max_length=250)


class BodySerializer(serializers.Serializer):
    """Body serializer"""

    action = serializers.CharField(max_length=40)
    payload = serializers.DictField()


class RequestSerializer(serializers.Serializer):
    """Request serializer"""

    headers = HeaderSerializer(many=True)
    body = BodySerializer()

    def create(self, validated_data):
        return to_object(validated_data)


class ResponseSerializer(serializers.Serializer):
    """Response serializer"""

    headers = HeaderSerializer(many=True)
    body = BodySerializer()

    status = serializers.IntegerField()

    def create(self, validated_data):
        return to_object(validated_data)
