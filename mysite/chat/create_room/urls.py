from django.urls import include, path

from . import views


app_name = "chat.create_room"
urlpatterns = [
    path("", views.create_room, name="create_room")  # ,
    # path("<str:room_name>/", include("chat.urls"))
]
