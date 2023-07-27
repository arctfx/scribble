from django.contrib.auth.backends import ModelBackend

from .models import Room, Player


class PlayerBackend(ModelBackend):
    # TBR
    def authenticate(self, request, username=None, room_id=None):
        # Check the username/password and return a user.
        try:
            room = Room.objects.get(pk=room_id)
            try:
                # Would not raise any exception, use get() instead:
                # player = Player.objects.filter(nickname=username, room__id=room_id).first()
                player = Player.objects.get(nickname=username, room__id=room_id)
                # TBR: add permission to play field in the Player model
                return player
            except Player.DoesNotExist:
                print("Player does not exist")  # debug
                player = Player.objects.create(nickname=username, room=room)
                player.save()
                return player
            except Player.MultipleObjectsReturned:  # should never raise this exception
                raise Exception("There are multiple players with those parameters")
        except Room.DoesNotExist:
            print("Room does not exist")  # debug
            return None

    def get_user(self, user_id):
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None
