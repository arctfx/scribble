from django.db import models
from django.db.models import IntegerField
from django.utils.crypto import get_random_string


# TBR
def generate_id():
    return get_random_string(length=8)


class Room(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default=generate_id())

    def __str__(self):
        return self.id


class Player(models.Model):
    # pk: user id (sessions generated)
    nickname = models.CharField(max_length=30)
    score: IntegerField = models.IntegerField(default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname


class Message(models.Model):
    sender = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    in_game = models.BooleanField(default=True)

    def __str__(self):
        return self.text
