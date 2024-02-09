from telebot import types

from constants import *
from db import db
from db.house import House
from utils import MatrixIndexPlacer


class View:
    def __init__(self, parse_mode="Markdown"):
        self.parse_mode = parse_mode
        pass

    def get_text(self):
        pass

    def get_keyboard(self):
        pass
