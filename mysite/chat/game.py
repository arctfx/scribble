import asyncio
import random

from .models import Room, Player
from .words import word_list


def custom_words(words: str):
    words_list = [' '.join(word.strip().split()) for word in words.split(',')]
    return words_list


class GameManager:
    def __init__(self, room_name: str, player_id: int):
        self.room = Room.objects.get(id=room_name)
        self.player_id = player_id
        self.is_playing = False  # TBR
        self.word = None

    @staticmethod
    def create_room(self):
        room = Room.create()
        return room

    async def start(self):
        asyncio.run(self.play_round())

    async def play_round(self):
        print("PLAY ROUND!")
        if self.room.painter_id is None:
            painter = Player.objects.filter(room__id=self.room_name).first()
            self.room.painter_id = painter.id
            assert self.room.painter_id is not None
            print(painter.id)

        # Choose random word
        self.word = random.choice(word_list)

        await asyncio.sleep(self.time_per_round)
