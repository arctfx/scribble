from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("admin/", admin.site.urls),
    path("create-room/", include("chat.create_room.urls")),
    path("join-room/", include("chat.join_room.urls")),
    path("room/", include("chat.urls"))
]
