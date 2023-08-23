from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone


def generate_id():
    return get_random_string(length=8)


class Room(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default=generate_id())
    rounds = models.IntegerField(default=3)  # number of rounds to be played
    time_per_round = models.IntegerField(default=45)  # in seconds
    timer = models.IntegerField(default=0)
    painter_id = models.IntegerField(default=None, null=True)
    drawingJSON = models.JSONField(default=list)
    in_progress = models.BooleanField(default=False)  # if the game is in progress
    word = models.TextField(default=None, null=True)

    def __str__(self):
        return self.id


class Player(models.Model):
    # pk: id
    nickname = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    # TBR: probably on_delete=CASCADE is not a good idea
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
    sender = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    in_game = models.BooleanField(default=True)  # TBR: not used

    def __str__(self):
        return self.text
