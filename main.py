import typing
import uuid

from config import telegram_token, lawyer_id
from telebot import types

from constants import *
from db.house import House
from db import db
from core.router import router
from core.context import Context, UpdateType
from db.invitation import Invitation
from db.invitation_participant import InvitationParticipant
from utils import Bot, MatrixIndexPlacer
from views.house_view import HouseView
from views.invintation_view import InvitationView
from views.tora_view import ToraView
from controllers.tora_controller import ToraController
import logging


logging.basicConfig(level=logging.WARNING)

bot = Bot(telegram_token)


def root_handler(m: types.Message):
    if m.text:
        route_handle_lambda(m=m, c=None, u_type=UpdateType.Command)

    user = db.get_user(m.from_user.id)
    if not user:
        db.create_user(m.from_user.id, m.from_user.full_name)


def c_root_handler(c: types.CallbackQuery):
    route_handle_lambda(m=None, c=c, u_type=UpdateType.Callback)


def route_handle_lambda(m: typing.Optional[types.Message], c: typing.Optional[types.CallbackQuery], u_type: UpdateType):
    context = Context(bot, m, c, u_type)
    router.handle(context)


@bot.message_handler(func=root_handler)
def _(_):
    return


@bot.callback_query_handler(func=c_root_handler)
def _(_):
    return


@bot.message_handler(commands=['start'])
def start_handler(m: types.Message):
    root_handler(m)

    bot.respond_to(m, "🫡")


@bot.message_handler(commands=['found'])
def found_handler(m: types.Message):
    root_handler(m)

    user = db.get_user(m.from_user.id)

    if user.money < 100:
        bot.respond_to(m, "📢У вас недостатньо шекелів! На створення дому треба 100!")
        return

    if m.text.count(' ') < 1:
        bot.respond_to(m, "🤕І шо? Назва дому де?")
        return

    name = m.text.split(" ", 1)[1]

    house = db.create_house(str(uuid.uuid4()), name)
    user.money -= 100
    user.house = house.id
    user.save()
    bot.respond_to(m, f"🪚Засновано дім \"{name}\".")


@bot.message_handler(commands=['registry'])
def registry_handler(m: types.Message):
    root_handler(m)

    kb = HouseView().get_keyboard()
    bot.respond_to(m, f"🏘Існуючі доми:", reply_markup=kb)


@bot.message_handler(commands=['ss'])
def ss_handler(m: types.Message):
    root_handler(m)

    if not m.reply_to_message:
        bot.respond_to(m, "🤕І шо?")
        return

    if m.from_user.id != lawyer_id:
        bot.respond_to(m, "🙇‍♀️Сорі, але це команда тільки для Юриста.")

    root_handler(m.reply_to_message)

    if not m.text.count(' '):
        bot.respond_to(m, f"🔪Успішно.")
        return

    invitation_id = int(m.text.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)
    user = db.get_user(m.reply_to_message.from_user.id)
    participant = InvitationParticipant(user=user, invitation_id=invitation.id)
    participant.save()
    invitation.participants.append(participant)
    invitation.save()

    bot.respond_to(m, f"🔪Інфузовано успішно.")


@bot.message_handler(commands=['pay'])
def house_handler(m: types.Message):
    root_handler(m)

    if not m.reply_to_message:
        bot.respond_to(m, "🤕І кому?")
        return

    if not m.text.count(' '):
        bot.respond_to(m, "🤕І скіко?")
        return

    amount = m.text.split(' ', 1)[1]
    if not amount.isnumeric():
        bot.respond_to(m, "🤕Шо?")
        return
    amount = int(amount)

    user = db.get_user(m.from_user.id)
    recipient = db.get_user(m.reply_to_message.from_user.id)

    if user.money < amount:
        bot.respond_to(m, "📢У вас нема стіки! Не грійте мене!")
        return

    if amount <= 0:
        bot.respond_to(m, "📢Штраф 40 шекелів за гойство.")
        return

    user.money -= amount
    recipient.money += amount

    user.save()
    recipient.save()

    bot.respond_to(m, "📢Гроші перекинуті успішно.")

print("Храмова система запущена. Успішного прогрівання.")
bot.infinity_polling()
