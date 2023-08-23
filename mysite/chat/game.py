import time
import random
from threading import Thread

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
            char_list[i] = "*"
    return ''.join(char_list)


# TBR: include custom words
def choose_word() -> str:
    # pool = [word_list, custom_words]
    # return random.choice(random.choices(pool, weights=map(len, pool))[0])
    return random.choice(word_list)


# wrapped around the Room class
class GameManager:
    def __init__(self, room_name: str, player_id: int):  # currently player_id = player's name
        self.room_name = room_name
        self.room = Room.objects.get(id=room_name)
        self.player = Player.objects.get(room__id=room_name, nickname=player_id)  # TBA: should get player by id
        self.round: int = 1  # should be moved to the Room model

    @classmethod
    def can_start(cls, room_name: str):
        return not Room.objects.get(id=room_name).in_progress

    # TBR: should be deprecated: same as time_left but it's a class method
    @classmethod
    def get_time(cls, room_name: str) -> int:
        return Room.objects.get(id=room_name).timer

    @property
    def word_encoded(self) -> str:
        return encode_word(self.room.word)

    @property
    def painter(self):
        return self.room.painter_id

    @property
    def time_left(self) -> int:
        return self.room.timer

    def guess(self, word: str) -> bool:
        if word == self.room.word:
            self.player.score += 100  # TBR: currently hardcoded
            self.player.save()

            painter = Player.objects.get(id=self.room.painter_id)
            painter.score += 50  # TBR: currently hardcoded
            painter.save()

            print("GUESSED WORD")
            return True
        else:
            return False

    def get_word(self, username: str) -> str:
        """
        Formats the mistery word depending on if the asking player is the painter or a guesser
        Painters will get the original word, while guessers will get an encoded version
        """
        if self.room.painter_id == self.player.id:
            return self.room.word
        else:
            return encode_word(self.room.word)

    def start(self):
        # if self.room.painter_id is None:
        #   painter = Player.objects.filter(room__id=self.room_name, online=True).first()
        print(self.player.nickname + " is starting this game")
        self.room.painter_id = self.player.id
        assert self.room.painter_id is not None
        self.room.in_progress = True
        self.room.word = choose_word()
        self.room.save()
        print(self.room.word)

        game_thread = Thread(target=self.play_round, args=[])
        game_thread.start()

    def end(self):
        self.room.timer = 0
        self.room.word = None
        self.room.in_progress = False
        self.room.save()

    def play(self):
        for r in range(1, self.room.rounds):
            self.play_round()
            time.sleep(5)  # intermediate time

    def play_round(self):
        print("PLAY ROUND!")

        self.room.timer = self.room.time_per_round
        self.room.save()
        for seconds in range(self.room.time_per_round, 0, -1):
            print(seconds)
            self.room.timer -= 1
            self.room.save()
            # await asyncio.sleep(1)
            time.sleep(1)

        self.end()
