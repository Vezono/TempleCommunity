import math

from telebot import TeleBot
from telebot import types


class Bot(TeleBot):
    def form_html_userlink(self, name, user_id):
        return f'<a href="tg://user?id={user_id}">{name}</a>'

    def respond_to(self, message, text, **kwargs):
        text = text.replace("_", "\\_")
        return self.send_message(message.chat.id, text, **kwargs)

    def edit_menu(self, callback: types.CallbackQuery, text, keyboard, **kwargs):
        return self.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=keyboard,
                                      **kwargs)


class MatrixIndexCounter:
    def __init__(self, width: int):
        self.width = max(width-1, 1)

        self.row = 0
        self.column = 0

    def current(self):
        return self.row, self.column

    def next(self):
        if self.column == self.width:
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        return self.current()

    def get_row(self, index):
        return math.floor(index / self.width)

    def reset(self, width: int = None):
        if width:
            self.width = max(width-1, 1)
        self.row = 0
        self.column = 0


class MatrixIndexPlacer:
    def __init__(self, width: int):
        self.counter = MatrixIndexCounter(width+1)

    def place(self, items: list):
        length = len(items)
        rows = self.counter.get_row(length-1)+1
        matrix = self.generate_matrix(rows)
        for i in range(length):
            row = self.counter.get_row(i)
            matrix[row].append(items[i])
        return matrix

    def generate_matrix(self, rows: int) -> list[list]:
        matrix = list()
        for i in range(rows):
            matrix.append(list())
        return matrix
