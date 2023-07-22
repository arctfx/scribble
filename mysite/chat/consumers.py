import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from .models import Room, Player
from channels.auth import login


class DrawingBoardConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "drawing-board_%s" % self.room_name
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)

            context = {"type": "drawing_board.update"}
            context.update(text_data_json)

            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, context)

        except ValueError as err:  # not needed to catch such exception
            print(err)

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def drawing_board_update(self, event):
        current_x = event["current_x"]
        current_y = event["current_y"]
        prev_x = event["prev_x"]
        prev_y = event["prev_y"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "current_x": current_x, "current_y": current_y, "prev_x": prev_x, "prev_y": prev_y
        }))


class LeaderboardConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "leaderboard_%s" % self.room_name

        player = self.scope["user"]
        player.online = True
        print(player.__str__() + " connected.")
        await sync_to_async(player.save)()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # Send message to room group
            await self.channel_layer.group_send(
                # text key-value pair is not used
                self.room_group_name, {"type": "leaderboard.update", "text": text_data}
            )

        except ValueError as err:  # not needed to catch such exception
            print(err)

    async def disconnect(self, code):
        player = self.scope["user"]
        player.online = False
        print(player.__str__() + " disconnected.")
        await sync_to_async(player.save)()
        await self.channel_layer.group_send(  # new
            # text key-value pair is not used
            self.room_group_name, {"type": "leaderboard.update", "text": "Player disconnected"}
        )

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Send the changed players list
    async def leaderboard_update(self, event):
        print("LEADERBOARD_UPDATE")
        players_query = await sync_to_async(Player.objects.filter)(room__id=self.room_name)  # .order_by("score")
        players = {}
        async for player in players_query:
            players[player.nickname] = {"score": player.score, "online": player.online}
        print(players)  # debug

        # Send signal to WebSocket
        await self.send(text_data=json.dumps(players))


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None
        # self.room: Room = None
        # self.player: Player = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # self.room = sync_to_async(Room.objects.get)(id=self.room_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            print(text_data)  # debug
            text_data_json = json.loads(text_data)

            message = text_data_json["message"]
            sender = text_data_json["sender"]

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message, "sender": sender}
            )

        except ValueError as err:
            print(err)

    # Receive message from room group
    async def chat_message(self, event):
        print("CHAT_MESSAGE")
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
