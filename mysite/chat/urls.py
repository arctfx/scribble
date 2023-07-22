from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("<str:room_name>/<str:user_name>/", views.login_room, name="login"),
    # TBR: fix regex in url: remove room_name and user_name - not necessary
    path("<str:room_name>/<str:user_name>/send_message/", views.send_message, name="send-message"),
    path("<str:room_name>/<str:user_name>/get_players/", views.get_players, name="get-players"),
    path("<str:room_name>/<str:user_name>/update_player/", views.update_player, name="update-player")
]
