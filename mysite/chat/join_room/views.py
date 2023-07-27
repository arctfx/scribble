from django.shortcuts import render


def join_room(request):
    return render(request, "join-room.html")
