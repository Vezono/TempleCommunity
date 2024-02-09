import typing
import uuid

from config import telegram_token, lawyer_id
from telebot import types

from constants import *
from db.house import House
from db import db
from core.router import router
from core.context import Context, UpdateType
from utils import Bot, MatrixIndexPlacer
from views.house_view import HouseView
from views.invintation_view import InvitationView
from views.tora_view import ToraView
from controllers.tora_controller import ToraController
import logging


logging.basicConfig(level=logging.INFO)

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

    bot.respond_to(m, f"🔪Успішно.")


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



@bot.message_handler(commands=['invite'])
def house_handler(m: types.Message):
    root_handler(m)

    if not m.reply_to_message:
        bot.respond_to(m, "🤕І шо?")
        return

    goi = db.get_user(m.reply_to_message.from_user.id)
    user = db.get_user(m.from_user.id)
    house = db.get_house(user.house)

    if goi.id == user.id:
        bot.respond_to(m, "🤯Геній?")
        return
    if not house:
        bot.respond_to(m, "👮В вас нема дому! Куди запрошувать?")
        return
    if user.status == 'goi':
        bot.respond_to(m, "🤕Ви гой, і Махновщину ще не побудували.")
        return

    invitation = None

    for existing_invitation in db.get_invitations(goi_id=goi.id):
        if existing_invitation.house_id == house.id:
            invitation = existing_invitation
            break

    if not invitation:
        invitation = db.create_invitation(goi_id=goi.id, house_id=house.id)

    i_view = InvitationView(invitation)
    bot.respond_to(m, i_view.get_text(), parse_mode="Markdown", reply_markup=i_view.get_keyboard())


@bot.message_handler(commands=['house'])
def profile_handler(m: types.Message):
    root_handler(m)
    user = db.get_user(m.from_user.id)

    house = db.get_house(user.house)

    if not house:
        bot.respond_to(m, "👮В вас нема дому!")
        return

    h_view = HouseView(house)

    tts = h_view.get_text()
    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['profile'])
def profile_handler(m: types.Message):
    root_handler(m)
    user = db.get_user(m.from_user.id)
    tts = user.profile()
    if user.status == 'goi':
        tts += (f"\n\n*Чому ти гой?*\n"
                f"Тому що ти новачок, і не пройшов \"стажування\". Почитай Тору. /tora.")
    if user.house == '':
        tts += (f"\n\n*Чому ти безхатько?*\n"
                f"Тому що не вступив в дім, або не створив свій!")
    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(GOI_DECLINE))
def invitation_pend(c: types.CallbackQuery):
    invitation_id = int(c.data.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)

    if not invitation:
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Запрошення №{invitation_id} вже загубили.", c.message.chat.id, c.message.id)

    user = db.get_user(c.from_user.id)
    if user.id != invitation.goi_id:
        bot.answer_callback_query(c.id, "👮🏻‍♂️Не ваша гойська справа", show_alert=False)
        return
    if invitation.status == 'decline':
        bot.answer_callback_query(c.id, "🤕Та вже всьо. Не жмакай", show_alert=False)
        return

    i_view = InvitationView(invitation)

    invitation.status = 'declined'
    invitation.save()

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                          parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(HOUSE_INFO_CALLBACK))
def house_info_callback(c: types.CallbackQuery):
    house_id = c.data.split('?', 1)[1]

    house = db.get_house(house_id)
    house_view = HouseView(house)
    if not house:
        kb = house_view.get_keyboard()
        bot.edit_message_text("🤕Дім не знайдено. Доступні доми надано нижче.", c.message.chat.id, c.message.id,
                              reply_markup=kb)

    tts = house_view.get_text()

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="↩️Назад до списку домів", callback_data=HOUSE_LIST_CALLBACK))

    bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="Markdown", reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data == '-')
def _(c: types.CallbackQuery):
    bot.answer_callback_query(c.id, "💳За жмак - 300 шекелів")


@bot.callback_query_handler(lambda c: c.data.startswith(GOI_ACCEPT))
def invitation_pend(c: types.CallbackQuery):
    invitation_id = int(c.data.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)

    if not invitation:
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Запрошення №{invitation_id} вже загубили.", c.message.chat.id, c.message.id)

    user = db.get_user(c.from_user.id)
    if user.id != invitation.goi_id:
        bot.answer_callback_query(c.id, "👮🏻‍♂️Не ваша гойська справа", show_alert=False)
        return
    if invitation.status == 'accepted':
        bot.answer_callback_query(c.id, "🤕Та вже всьо. Не жмакай", show_alert=False)
        return

    i_view = InvitationView(invitation)

    invitation.status = 'accepted'
    invitation.save()

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                          parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(INVITATION_REJECT_CALLBACK))
def invitation_pend(c: types.CallbackQuery):
    invitation_id = int(c.data.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)

    if not invitation:
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Запрошення №{invitation_id} вже загубили.", c.message.chat.id, c.message.id)

    user = db.get_user(c.from_user.id)
    participant = invitation.get_participant(user.id)
    if not participant:
        bot.answer_callback_query(c.id, "👮🏻‍♂️Не ваша гойська справа", show_alert=False)
        return
    if participant.status == 'rejected':
        bot.answer_callback_query(c.id, "🤕Та вже всьо. Не жмакай", show_alert=False)
        return

    i_view = InvitationView(invitation)
    participant.status = 'rejected'
    participant.save()

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                          parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(INVITATION_PEND_CALLBACK))
def invitation_pend(c: types.CallbackQuery):
    invitation_id = int(c.data.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)

    if not invitation:
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Запрошення №{invitation_id} вже загубили.", c.message.chat.id, c.message.id)

    user = db.get_user(c.from_user.id)
    participant = invitation.get_participant(user.id)
    if not participant:
        bot.answer_callback_query(c.id, "👮🏻‍♂️Не ваша гойська справа", show_alert=False)
        return
    if participant.status == 'pending':
        bot.answer_callback_query(c.id, "🤕Та вже всьо. Не жмакай", show_alert=False)
        return

    i_view = InvitationView(invitation)
    participant.status = 'pending'
    participant.save()

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                          parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(INVITATION_APPROVE_CALLBACK))
def invitation_approve(c: types.CallbackQuery):
    invitation_id = int(c.data.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)

    if not invitation:
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Запрошення №{invitation_id} вже загубили.", c.message.chat.id, c.message.id)

    user = db.get_user(c.from_user.id)
    participant = invitation.get_participant(user.id)
    if not participant:
        bot.answer_callback_query(c.id, "👮🏻‍♂️Не ваша гойська справа", show_alert=False)
        return
    if participant.status == 'approved':
        bot.answer_callback_query(c.id, "🤕Та вже всьо. Не жмакай", show_alert=False)
        return

    i_view = InvitationView(invitation)
    participant.status = 'approved'
    participant.save()

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                          parse_mode="Markdown")


print("Храмова система запущена. Успішного прогрівання.")
bot.infinity_polling()
