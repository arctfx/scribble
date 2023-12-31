from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/leaderboard/(?P<room_name>\w+)/$", consumers.LeaderboardConsumer.as_asgi()),
    re_path(r"ws/drawing-board/(?P<room_name>\w+)/$", consumers.DrawingBoardConsumer.as_asgi()),
    re_path(r"ws/game/(?P<room_name>\w+)/$", consumers.GameConsumer.as_asgi())
]
