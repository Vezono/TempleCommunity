import typing

from telebot import types

from constants import *
from db import db
from db.house import House
from utils import MatrixIndexPlacer
from core.view import View


class HouseView(View):
    def __init__(self, house: typing.Optional[House] = None):
        super().__init__()
        self.house = house

    def get_keyboard(self):
        buttons = list()
        kb = types.InlineKeyboardMarkup()

        for house in House.objects():
            buttons.append(
                types.InlineKeyboardButton(text=house.name, callback_data=f"{HOUSE_INFO_CALLBACK}?{house.id}")
            )

        mip = MatrixIndexPlacer(2)
        matrix = mip.place(buttons)

        for row in matrix:
            kb.add(*row)

        return kb

    def get_text(self):
        jews = list(db.get_jews(self.house.id))
        gois = list(db.get_gois(self.house.id))

        if not jews:
            jews_names = "відсутні"
        else:
            jews_names = "\n"
            for jew in jews:
                jews_names += f"- {jew.name}\n".replace("_", "\\_")

        if not gois:
            gois_names = "відсутні"
        else:
            gois_names = "\n"
            for goi in gois:
                gois_names += f"- {goi.name}\n".replace("_", "\\_")

        tts = f"*{self.house.name.replace("_", "\\_")}*\n"
        tts += f"📁Опис: {self.house.description.replace("_", "\\_")}\n\n"
        tts += f"✡️Жиди: {jews_names}\n"
        tts += f"🦥Гої: {gois_names}\n\n"
        tts += (f"💰Баланс: {self.house.money}\n"
                f"⚖Прибуток жидам: {self.house.ratio}%\n")
        return tts
