import requests
import json
from random import randrange
from random import shuffle
from config import db as db
from model.dice import Dice
from datetime import datetime
from datetime import timedelta

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, unique=False, nullable=False)
    finished = db.Column(db.Boolean, unique=False, nullable=False)
    letters = db.Column(db.String(24), unique=False, nullable=False)
    words = db.Column(db.String(), unique=False, nullable=False)
    start_time = db.Column(db.DateTime(), unique=False, nullable=False)
    end_time = db.Column(db.DateTime(), unique=False, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref=db.backref('Game', lazy=True))

    board = [
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', '']
    ]

    word_list = []

    current_input = ""
    current_letters = []

    message = ""

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.score = 0
        self.finished = False
        self.words = ''
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=3)
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

    def submit_letter(self, current_input, current_letters, x, y, prev_x, prev_y):
        if self.is_input_already_used(x, y, current_letters):
            self.message = "Invalid action, this letter has already been played this turn"
        elif (prev_x is None and prev_y is None) or self.is_input_connected(x, y, prev_x, prev_y):
            self.current_input = current_input + self.board[x][y]
            return self.current_input
        else:
            self.message = "Invalid action, all selected letters must be connected"

    def generate_word_list(self):
        self.word_list = self.words.split(',')

    def submit_word(self, word):
        if self.words.__len__() > 0:
            self.words += ","
        self.words += word

    def increase_score(self, score):
        self.score += score

    def set_message(self, message):
        self.message = message

    def is_there_still_time(self):
        if (self.end_time - datetime.now()).total_seconds() > 0:
            return True
        else:
            return False

    def has_word_been_played(self, word):
        if word in self.words.split(','):
            return True
        return False

    @staticmethod
    def is_input_already_used(x,y, current_letters):
        if current_letters:
            if str(x) + str(y) in current_letters:
                return True
        return False

    @staticmethod
    def is_input_connected(x, y, prev_x, prev_y):
        is_connected = False
        if prev_x + 1 == x:
            if prev_y + 1 == y:
                is_connected = True
            if prev_y - 1 == y:
                is_connected = True
            if prev_y == y:
                is_connected = True
        if prev_x - 1 == x:
            if prev_y + 1 == y:
                is_connected = True
            if prev_y - 1 == y:
                is_connected = True
            if prev_y == y:
                is_connected = True
        if prev_x == x:
            if prev_y + 1 == y:
                is_connected = True
            if prev_y - 1 == y:
                is_connected = True
            if prev_y == y:
                is_connected = False
        return is_connected

