from channels.routing import route, route_class
from .consumers import ws_connect, ws_receive, ws_disconnect
from .consumers_ import lobby

channel_routing = [
    route_class(lobby.LobbyConsumer,
                path=r"^/lobby/(?P<id>[a-z0-9.-]*)/$"),
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),
]
