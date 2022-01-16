import requests
import json
from random import randrange
from random import shuffle
from config import db as db
from model.dice import Dice


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, unique=False, nullable=False)
    finished = db.Column(db.Boolean, unique=False, nullable=False)
    letters = db.Column(db.String(24), unique=False, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref=db.backref('Game', lazy=True))

    board = [
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', '']
    ]

    time = 180000

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.score = 0
        self.finished = False
        self.generate_letters()
        self.generate_board()

    def generate_letters(self):
        dices = Dice.query.all()
        shuffle(dices)
        self.letters = ""
        for dice in dices:
            print(len(dices))
            i = randrange(len(dice.letters))
            self.letters += dice.letters[i]
        self.letters

    def generate_board(self):
        i = 0
        y = 0
        while y < 4:
            x = 0
            while x < 4:
                self.board[y][x] = self.letters[i]
                x += 1
                i += 1
            y += 1

    def is_there_still_time(self):
        if self.time > 0:
            return True
        else:
            return False

    def is_input_connected(self, player_input):
        return True

