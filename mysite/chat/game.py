import asyncio
import time
import random
import threading

from .models import Room, Player
from .words import word_list


def string_to_words_list(words: str):
    words_list = [
        ' '.join(word.strip().split())  # remove all unnecessary whitespaces
        for word in words.lower().split(',')  # separate words with comma and make all letters lower-case
        if word.replace(" ", "").isalpha()  # check if the word contains only whitespaces and letters
    ]
    return words_list


class GameManager:
    def __init__(self, room_name: str, player_id: int):
        self.room = Room.objects.get(id=room_name)
        self.player_id = player_id
        self.in_progress = False
        self.word = None
        self.seconds_per_round = 10
        # self.timer = Timer

    # TBR: Probably not used
    @staticmethod
    def create_room():
        room = Room.create()
        return room

    def start(self):
        asyncio.run(self.play())

    def end(self):
        pass

    async def play(self):
        self.in_progress = True
        loop = asyncio.get_running_loop()
        threading.Thread(target=self.game_thread, args=(loop,)).start()
        self.in_progress = False

    def game_thread(self, loop):
        coro = self.play_round()
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        future.result()
        print("Round finished")

    async def play_round(self):
        print("PLAY ROUND!")
        """if self.room.painter_id is None:
            painter = Player.objects.filter(room__id=self.room_name).first()
            self.room.painter_id = painter.id
            assert self.room.painter_id is not None
            print(painter.id)
        """

        # Choose random word
        self.word = random.choice(word_list)
        print(self.word)

        seconds_remaining = self.seconds_per_round

        while seconds_remaining >= 0:
            print(seconds_remaining)
            await asyncio.sleep(1)
            # time.sleep(1)
            seconds_remaining -= 1
