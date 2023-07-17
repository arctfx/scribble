from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("<str:room_name>/<str:user_name>/", views.login_room, name="login"),
    path("<str:room_name>/<str:user_name>/send_message/", views.send_message, name="send-message") # fix regex in url
]

rooms: list[str] = [
    "lobby",
]
