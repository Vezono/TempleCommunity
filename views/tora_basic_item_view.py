from telebot import types

from constants import *
from core.view import View


class ToraBasicItemView(View):
    def __init__(self, text: str, parse_mode="Markdown"):
        super().__init__(parse_mode=parse_mode)
        self.text = text

    def get_keyboard(self):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="↩️Назад до Тори", callback_data=MAIN_HELP_CALLBACK))

        return kb

    def get_text(self):
        return self.text
