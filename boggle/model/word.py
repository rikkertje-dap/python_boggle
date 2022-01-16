import requests
import json


class Word:

    def __init__(self, word):
        self._word = word
        self._definition = ""
        self._type = ""

    @property
    def word(self):
        return self._word

    @property
    def definition(self):
        return self._definition

    @property
    def type(self):
        return self._type

    @definition.setter
    def set_definition(self, value):
        self._definition = value

    @type.setter
    def set_definition(self, value):
        self._type = value

    def is_word_valid(self):
        result = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + self._word)
        obj = json.loads(result.text)
        if isinstance(obj, list):
            if "word" in obj[0]:
                print(obj[0])
                return True
        else:
            return False
