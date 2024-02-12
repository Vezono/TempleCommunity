from telebot import types

from constants import *
from core.view import View


class BasicTextView(View):
    def __init__(self, text: str):
        super().__init__(parse_mode=parse_mode)
        self.text = text

    def get_keyboard(self):
        kb = types.InlineKeyboardMarkup()
        return kb

    def get_text(self):
        return self.text
