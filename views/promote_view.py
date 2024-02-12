import typing

from telebot import types

from constants import *
from db import db
from db.house import House
from utils import MatrixIndexPlacer
from core.view import View


class PromoteView(View):
    def __init__(self):
        super().__init__()

    def get_keyboard(self):
        kb = types.InlineKeyboardMarkup()

        kb.add(
            types.InlineKeyboardButton(text="Кнопки євреїв:", callback_data="-")
        )

        kb.add(
            types.InlineKeyboardButton(
                text=f"✅Промоут",
                callback_data=f"{INVITATION_APPROVE_CALLBACK} {self.invitation.id}"
            ),
            types.InlineKeyboardButton(
                text=f"⏳Подумати",
                callback_data=f"{INVITATION_PEND_CALLBACK} {self.invitation.id}"
            ),
            types.InlineKeyboardButton(
                text=f"❌Відхилити",
                callback_data=f"{INVITATION_REJECT_CALLBACK} {self.invitation.id}"
            )
        )

        return kb

    def get_info_text(self):
        goi_text = 'Єврей'
        if self.goi.status == 'goi':
            goi_text = 'Гой'

        tts = (f"*📇Запрошення* №{self.invitation.id}\n"
               f"🏛Дім: {self.house.name}\n"
               f"👤{goi_text}: {self.goi.name}\n\n")

        return tts.replace("_", "\\_")

    def get_text(self):
        tts = self.get_info_text()
        tts += f"*✍️Підписи євреїв*:\n"

        for participant in self.invitation.participants:
            if participant.status == 'pending' or not participant.status:
                emoji = "⏳"
            elif participant.status == "approved":
                emoji = "✅"
            elif participant.status == "rejected":
                emoji = "❌"
            else:
                emoji = "🤕"
            tts += f"{emoji}{participant.user.name}\n".replace("_", "\\_")

        if self.invitation.status == 'pending':
            tts += "\n⏳Вступаючий ще думає."
        if self.invitation.status == 'accepted':
            tts += "\n✅Вступаючий прийняв запрошення."
        if self.invitation.status == 'declined':
            tts += "\n❌Вступаючий відхилив запрошення."

        if self.invitation.ready:
            tts += "\n♻️Запрошення затверджено."

        return tts.replace("_", "\\_")



