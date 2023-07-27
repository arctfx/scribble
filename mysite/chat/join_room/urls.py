from django.urls import include, path

from . import views


# app_name = "chat.join_room"
urlpatterns = [
    path("", views.join_room, name="join_room"),
    path("<str:room_name>/", include("chat.urls"))
]
