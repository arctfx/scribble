from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import IntegerField
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.utils import timezone


# TBR
def generate_id():
    return get_random_string(length=8)


class Room(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default=generate_id())

    def __str__(self):
        return self.id


class Player(models.Model):
    # pk: id
    nickname = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    online = models.BooleanField(default=False)
    # Player should
    # AbstractBaseUser requires default password

    # django.contrib.auth.checks requires these fields:
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["room"]  # TBR

    def __str__(self):
        return self.nickname

    # django.contrib.auth.checks requires this property
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    # django.contrib.auth.checks requires this property
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class Message(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    in_game = models.BooleanField(default=True)

    def __str__(self):
        return self.text
