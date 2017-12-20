from channels.routing import route, route_class

from .consumers import ChatConsumer


channel_routing = [
    ChatConsumer.as_route(path=r'common/rooms/(?P<room_id>[0-9]{1,20})$'),
]
