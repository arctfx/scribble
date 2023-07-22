from models import *
import time


class Draw:
    def __init__(self, word: str):
        self.clock = time.clock()
        self.word = word


class Game:
    def __init__(self, rounds: int, number_of_players: int):
        self.rounds = rounds
