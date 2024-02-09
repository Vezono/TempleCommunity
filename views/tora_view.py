from telebot import types

from constants import *
from core.view import View


class ToraView (View):
    def __init__(self):
        super().__init__()

    def get_keyboard(self):
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(text="👮‍♂️Правила Храму", callback_data=CHAT_RULES_CALLBACK),
            types.InlineKeyboardButton(text="🏅Ролі членів Храму", callback_data=ROLE_HELP_CALLBACK),
        )
        kb.add(
            types.InlineKeyboardButton(text="🏡Доми", callback_data=HOUSE_HELP_CALLBACK),
            types.InlineKeyboardButton(text="✡️Жиди та гої", callback_data=JEWISH_HELP_CALLBACK)
        )
        kb.add(
            types.InlineKeyboardButton(text="💻Команди (як щось зробити?)", callback_data=COMMANDS_HELP_CALLBACK)
        )
        kb.add(
            types.InlineKeyboardButton(text="❓Інші питання", callback_data=WHY_HELP_CALLBACK)
        )

        return kb

    def get_text(self):
        return (f"📖Тора редакції {VERSION}:\n\n"
               f"Вітаю, я Храмова Варта, або просто Варта - електронна система Храмового лору, традицій та приколів. "
               f"В цьому розділі ви можете отримати допомогу по різним темам системи.")
