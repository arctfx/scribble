from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Player
from .models import Message
from .models import Room


def index(request, redirected=False):
    context = {"bad_room_id": redirected}
    return render(request, "chat/index.html", context)


def login_room(request, room_name, user_name):
    room_obj = Room.objects.filter(pk=room_name).first()
    if room_obj:
        player_obj = Player.objects.filter(nickname=user_name, room=room_obj).first()
        if player_obj is None:
            player_obj = Player(nickname=user_name, room=room_obj)
            player_obj.save()
        latest_messages = Message.objects.filter(sender__room__id=room_name)
        context = {"user_name": user_name,
                   "room_name": room_name,
                   "latest_messages": latest_messages}
        return render(request, "chat/room.html", context)
    else:
        return index(request, True)


def room(request, room_name):
    # get_object_or_404(Room, pk=room_name)
    room_obj = Room.objects.filter(pk=room_name).first()
    if room_obj:
        latest_messages = Message.objects.filter(sender__room__id=room_name)
        context = {"room_name": room_name,
                   "latest_messages": latest_messages}
        return render(request, "chat/room.html", context)
    else:
        return index(request, True)


@csrf_exempt
def send_message(request, room_name, user_name):
    # TBR: send player id rather than player's nickname
    sender_obj = Player.objects.filter(nickname=request.POST["sender"]).first()
    message = Message(sender=sender_obj, text=request.POST["text"])
    message.save()
    return HttpResponse("Message sent!")
