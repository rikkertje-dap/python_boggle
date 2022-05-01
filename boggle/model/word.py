import requests
import json


class Word:

    def __init__(self, word):
        self._word = word
        self._definition = ""
        self._type = ""
        self._score = 0
        self.get_word_data(word)

    def __str__(self):
        return " word: " + self.word + " definition: " + self.definition

    @property
    def word(self):
        return self._word

    @property
    def definition(self):
        return self._definition

    @property
    def type(self):
        return self._type

    @property
    def score(self):
        return self._score

    @definition.setter
    def set_definition(self, value):
        self._definition = value

    @type.setter
    def set_type(self, value):
        self._type = value

    def calculate_score(self):
        if len(self.word) >= 8:
            self._score = 11
        elif len(self.word) == 7:
            self._score = 5
        elif len(self.word) == 6:
            self._score = 3
        elif len(self.word) == 5:
            self._score = 2
        elif len(self.word) >= 3 or len(self.word) <= 4:
            self._score = 1

    def get_word_data(self, word):
        result = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
        obj = json.loads(result.text)
        if isinstance(obj, list):
            if "word" in obj[0]:
                word_object = obj[0]
                meanings = word_object["meanings"][0]
                definition_object = meanings["definitions"][0]
                self._definition = definition_object["definition"]
                self._type = meanings["partOfSpeech"]
                self.calculate_score()
        return self

    @staticmethod
    def is_valid_word(word):
        result = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
        obj = json.loads(result.text)
        if isinstance(obj, list):
            if "word" in obj[0]:
                return True
        else:
            return False