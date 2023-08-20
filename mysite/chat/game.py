import asyncio
import time
import random
from threading import Thread

import datetime
# now = datetime.datetime.now()

from .models import Room, Player
from .words import word_list


def string_to_list_of_words(words: str) -> list[str]:
    words_list = [
        ' '.join(word.strip().split())  # remove all unnecessary whitespaces
        for word in words.lower().split(',')  # separate words with comma and make all letters lower-case
        if word.replace(' ', '').isalpha()  # check if the word contains only whitespaces and letters
    ]
    return words_list


# strings are immutable in python
def encode_word(word: str) -> str:
    char_list = list(word)
    for i in range(1, len(char_list)):
        if not char_list[i].isspace():
            char_list[i] = " _"
        else:
            char_list[i] = "  "
    return ''.join(char_list)


# TBR: include custom words
def choose_word() -> str:
    # pool = [word_list, custom_words]
    # return random.choice(random.choices(pool, weights=map(len, pool))[0])
    return random.choice(word_list)


class GameManager:
    def __init__(self, room_name: str, player_id: int):
        self.room_name = room_name
        self.room = Room.objects.get(id=room_name)   # TBR: maybe unused
        self.player_id = player_id
        self.in_progress = False  # TBR: maybe unused
        self.word: str = None
        self.seconds_per_round = 10
        self.rounds = 3
        self.round = 1
        self.painter_id = None
        self.timer = 0

    # TBR: Probably not used
    @staticmethod
    def create_room():
        room = Room.create()
        return room

    def start(self) -> dict:
        # response = {}
        if self.room.painter_id is None:
            painter = Player.objects.filter(room__id=self.room_name, online=True).first()
            self.room.painter_id = painter.id
            assert self.room.painter_id is not None
        # response.update({"painter": painter.id})

        self.word = choose_word()
        # response.update({"word": encode_word(self.word)})

        self.in_progress = True
        game_thread = Thread(target=self.play_round, args=[])
        game_thread.start()

        # return response

    def end(self):
        self.in_progress = False

    def play(self):
        for r in range(1, self.rounds):
            self.play_round()
            time.sleep(5)  # intermediate time

    def play_round(self):
        print("PLAY ROUND!")

        self.timer = self.seconds_per_round
        for seconds in range(self.seconds_per_round, 0, -1):
            print(seconds)
            self.timer -= 1
            # await asyncio.sleep(1)
            time.sleep(1)

        self.end()
