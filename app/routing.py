from channels.routing import include

from .consumers import NotFoundConsumer


channel_routing = [
    # WS v1
    include('common.routing.channel_routing', path=r'^/ws/v1/'),
]

# 404 error
channel_routing += [
    NotFoundConsumer.as_route(path=r'^'),
]
