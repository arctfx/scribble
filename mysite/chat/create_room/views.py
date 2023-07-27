from django.shortcuts import render


def create_room(request):
    return render(request, "create-room.html")
