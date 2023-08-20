from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate

from .models import Room, Player, Message
from .authentication import PlayerBackend
from .game import GameManager
from .game import encode_word


def index(request, redirected=False):
    context = {"bad_room_id": redirected}
    return render(request, "chat/index.html", context)


def create_room(request, user_name):
    room_obj = Room.objects.create()
    room_obj.save()
    user = Player.objects.create(nickname=user_name, room=room_obj)
    user.save()
    login(request, user, backend="chat.authentication.PlayerBackend")
    return redirect(f"/room/{room_obj.id}/{user_name}")


# TBR: wrong room crashes the server
def login_room(request, room_name, user_name):
    room_obj = Room.objects.filter(pk=room_name).first()
    if room_obj:
        user = authenticate(request, room_id=room_name, username=user_name)  # new
        print(user)  # debug
        if user is not None:
            login(request, user, backend="chat.authentication.PlayerBackend")
            player_obj = Player.objects.filter(nickname=user_name, room=room_obj).first()
            if player_obj is None:
                player_obj = Player(nickname=user_name, room=room_obj)
                player_obj.save()
            latest_messages = Message.objects.filter(sender__room__id=room_name).order_by("timestamp")
            context = {"user_name": user_name,
                       "room_name": room_name,
                       "latest_messages": latest_messages}
            # Redirect to a success page.
            return render(request, "chat/room.html", context)
        else:
            raise Exception("User does not exist")
    else:
        return index(request, True)


# TBR: Probably not used at all
"""
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
"""


@csrf_exempt
def send_message(request, room_name, user_name):
    # TBR: send player id rather than player's nickname
    sender_obj = Player.objects.filter(nickname=request.POST["sender"]).first()
    message = Message(sender=sender_obj, text=request.POST["text"])
    message.save()
    return HttpResponse("Message sent!")


# TBR: room_name & user_name arguments are required by the url format, although are not used
# @csrf_exempt
# @requires_csrf_token
@csrf_exempt
def update_player(request, room_name, user_name):
    # TBR: send player id rather than player's nickname
    print(request.POST)
    player_obj = Player.objects.filter(nickname=request.POST["nickname"]).first()
    # player_obj__score = request.POST["score"]
    player_obj.online = True if request.POST["online"] == "true" else False
    player_obj.save()
    # TBR add websocket and url as response instead of plain text
    return HttpResponse("Player updated!")


# TBR: room_name & user_name arguments are required by the url format, although are not used
@csrf_exempt
def get_players(request, room_name, user_name):
    # TBR: filter by room id AND order by online=true
    player_list = Player.objects.filter(room__id=request.GET["room_name"]).order_by("score")
    players = []
    for player in player_list:
        players.append({"nickname": player.nickname, "score": player.score, "online": player.online})
    # Passing non-dictionary data, therefore safe=False
    return JsonResponse(players, safe=False)


# TBR: request argument is required by the url format, although is not used
@csrf_exempt
def start_game(request, room_name, user_name):
    print("GAME STARTED")
    game = GameManager(room_name, user_name)
    game.start()
    response = {"timer": game.seconds_per_round,
                "round": game.round,
                "painter": game.painter_id,
                "word": encode_word(game.word)}
    return JsonResponse(response)


@csrf_exempt
def get_drawing(request, room_name, user_name):
    room = Room.objects.get(id=room_name)
    drawing_json = room.drawingJSON
    return JsonResponse(drawing_json, safe=False)
