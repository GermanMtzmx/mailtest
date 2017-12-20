from channels.generic.websockets import WebsocketConsumer
from channels import Group


class ChatConsumer(WebsocketConsumer):
    """Chat consumer"""

    channel_session_user = True

    def connect(self, message, room_id=None, **kwargs):
        super(self.__class__, self).connect(message, **kwargs)

        Group('room-%s' % room_id).add(message.reply_channel)

    def receive(self, text=None, bytes=None, room_id=None):
        Group('room-%s' % room_id).send({'text': text})

    def disconnect(self, message, room_id=None):
        Group('room-%s' % room_id).discard(message.reply_channel)
