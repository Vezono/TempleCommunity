import typing

from enum import Enum, auto

from telebot import types

from utils import Bot


class UpdateType(Enum):
    Command = auto()
    Callback = auto()


class Context:
    def __init__(self, bot: Bot, message: typing.Optional[types.Message], callback: typing.Optional[types.CallbackQuery], type: UpdateType):
        self.bot = bot
        self.message = message
        self.callback = callback
        self.type = type

    def __str__(self):
        return (f"({self.message.text if self.message else ''}, {self.callback.data if self.callback else ''},"
                f" {self.type})")
