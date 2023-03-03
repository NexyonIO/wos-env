import json


class Config:
    def __init__(self):
        self.values = json.load(open("config.json"))
