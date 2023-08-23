from django.urls import path

from . import views


urlpatterns = [
    path("create/<str:user_name>/", views.create_room, name="create-room"),
    # path("<str:room_name>/", views.room, name="room"),  # TBR: obsolete
    path("<str:room_name>/<str:user_name>/", views.login_room, name="login"),
    # TBR: edit urls
    path("<str:room_name>/<str:user_name>/send_message/", views.send_message, name="send-message"),
    path("<str:room_name>/<str:user_name>/get_players/", views.get_players, name="get-players"),
    path("<str:room_name>/<str:user_name>/update_player/", views.update_player, name="update-player"),
    path("<str:room_name>/<str:user_name>/start_game/", views.start_game, name="start-game"),
    path("<str:room_name>/<str:user_name>/get_drawing/", views.get_drawing, name="get_drawing"),
    path("<str:room_name>/<str:user_name>/guess_word/", views.guess_word, name="guess_word"),
    path("<str:room_name>/<str:user_name>/get_word/", views.get_word, name="get_word")
]
