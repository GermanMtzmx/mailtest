import json

from django.utils.translation import gettext_lazy as _

from channels.generic.websockets import WebsocketConsumer


class NotFoundConsumer(WebsocketConsumer):
    """Not found consumer"""

    def connect(self, message, **kwargs):
        super(self.__class__, self).connect(message, **kwargs)

        message.reply_channel.send({
            'text': json.dumps({
                'detail': _('Not found.')
            })
        })

        self.close()
