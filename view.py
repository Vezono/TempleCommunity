from telebot import types

from constants import *
from db import db
from db.house import House
from utils import MatrixIndexPlacer


class View:
    def __init__(self):
        pass

    def house_list_keyboard(self):
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

    def house_info_text(self, house):
        jews = list(db.get_jews(house.id))
        gois = list(db.get_gois(house.id))

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

        tts = f"*{house.name.replace("_", "\\_")}*\n"
        tts += f"📁Опис: {house.description.replace("_", "\\_")}\n\n"
        tts += f"✡️Жиди: {jews_names}\n"
        tts += f"🦥Гої: {gois_names}\n\n"
        tts += (f"💰Баланс: {house.money}\n"
                f"⚖Прибуток жидам: {house.ratio}%\n")
        return tts

    def tora(self):
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(text="👮‍♂️Правила Храму", callback_data=CHAT_RULES_CALLBACK),
            types.InlineKeyboardButton(text="🏅Ролі членів Храму", callback_data=ROLE_HELP_CALLBACK),
        )
        kb.add(
            types.InlineKeyboardButton(text="🏡Доми", callback_data=HOUSE_HELP_CALLBACK),
            types.InlineKeyboardButton(text="✡️Жиди та гої", callback_data=JEWISH_HELP_CALLBACK)
        )

        tts = (f"📖Тора редакції {VERSION}:\n\n"
               f"Вітаю, я Храмова Варта, або просто Варта - електронна система Храмового лору, традицій та приколів. "
               f"В цьому розділі ви можете отримати допомогу по різним темам системи.")
        return kb, tts
