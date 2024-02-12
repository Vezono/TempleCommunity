from telebot import types

from constants import *
from db import db
from core.view import View
from db.invitation import Invitation
from db.invitation_participant import InvitationParticipant


class InvitationsView(View):
    def __init__(self):
        super().__init__()

    def get_keyboard(self):
        mp = MatrixIndexPlacer(4)
        buttons = []
        kb = types.InlineKeyboardMarkup()

        for invitation in Invitation.objects():
            buttons.append(types.InlineKeyboardButton(
                text=f"№{invitation.id}", callback_data=f"{VIEW_INVITATION_CALLBACK} {invitation.id}"
            ))

        rows = mp.place(buttons)
        for row in rows:
            kb.add(*row)

        return kb

    def get_text(self):
        return "📃Усі активні запрошення: "
