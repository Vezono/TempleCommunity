# цей файл створив КОЗІЧ (я тут нідочого)
from core.controller import Controller
from core.router import router
from constants import *
from core.context import Context
from views.invitations_view import InvitationsView
from views.invintation_view import InvintationView
from views.tora_basic_item_view import ToraBasicItemView
from views.basic_text_view import BasicTextView
from db.invitation import Invitation
from db.invitation_participant import InvitationParticipant

from db import db

class HouseController(Controller):
    def __init__(self):
        super().__init__()
    
    @router.register_command('house')
    def house_handler(context: Context):
        user = db.get_user(context.message.from_user.id)

        house = db.get_house(user.house)

        if not house:
            return BasicTextView("👮В вас нема дому!")

        return HouseView(house)

    @router.register_command('profile')
    def house_handler(context: Context):
        user = db.get_user(context.message.from_user.id)
        tts = user.profile()
        if user.status == 'goi':
            tts += (f"\n\n*Чому ти гой?*\n"
                    f"Тому що ти новачок, і не пройшов \"стажування\". Почитай Тору. /tora.")
        if user.house == '':
            tts += (f"\n\n*Чому ти безхатько?*\n"
                    f"Тому що не вступив в дім, або не створив свій!")
                    
        return BasicTextView(tts)
    
    @router.register_callback(GOI_DECLINE)
    def invitation_pend(context: Context):
        invitation_id = int(context.callback.data.split(' ', 1)[1])
        invitation = db.get_invitation(invitation_id)

        if not invitation:
            context.answer_callback_query("🤕Ойойой...")
            return BasicTextView(f"🤕Запрошення №{invitation_id} вже загубили.")

        user = db.get_user(c.from_user.id)
        if user.id != invitation.goi_id:
            context.answer_callback_query("👮🏻‍♂️Не ваша гойська справа")
            return
        if invitation.status == 'decline':
            context.answer_callback_query("🤕Та вже всьо. Не жмакай")
            return

        invitation.status = 'declined'
        invitation.save()

        return InvitationView(invitation)
        
    @router.register_callback(HOUSE_INFO_CALLBACK)
    def house_info_callback(context: Context):
        house_id = context.callback.data.split('?', 1)[1]

        house = db.get_house(house_id)
        
        return HouseView(house, "🤕Дім не знайдено. Доступні доми надано нижче.")
    
    @router.register_callback('-')
    def blank_handler(context: Context):
        context.answer_callback_query(c.id, "💳За жмак - 300 шекелів")
    
    @router.register_callback(GOI_ACCEPT)
    def invitation_pend(context: Context):
        invitation_id = int(c.data.split(' ', 1)[1])
        invitation = db.get_invitation(invitation_id)

        if not invitation:
            context.answer_callback_query("🤕Ойойой...")
            return BasicTextView(f"🤕Запрошення №{invitation_id} вже загубили.")

        user = db.get_user(c.from_user.id)
        if user.id != invitation.goi_id:
            context.answer_callback_query("👮🏻‍♂️Не ваша гойська справа")
            return
        if invitation.status == 'decline':
            context.answer_callback_query("🤕Та вже всьо. Не жмакай")
            return

        i_view = InvitationView(invitation)

        invitation.status = 'accepted'
        invitation.save()

        if invitation.ready:
            goi = db.get_user(invitation.goi_id)
            goi.house = invitation.house_id
            goi.save()
            invitation.delete()
            tts = i_view.get_info_text()
            tts += "\n♻Одноголосно прийнято. Заявка закрита."
            bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="Markdown")
            return

        bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                            parse_mode="Markdown")



@bot.callback_query_handler(lambda c: c.data.startswith(GOI_ACCEPT))
def invitation_pend(c: types.CallbackQuery):


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
        return

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

    if invitation.ready:
        goi = db.get_user(invitation.goi_id)
        goi.house = invitation.house_id
        goi.save()
        invitation.delete()
        tts = i_view.get_info_text()
        tts += "\n♻Одноголосно прийнято. Заявка закрита."
        bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="Markdown")
        return

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=i_view.get_keyboard(),
                          parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(INVITATION_LIST_CALLBACK))
def invitation_approve(c: types.CallbackQuery):
    tts = "📃Усі активні запрошення: "

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

    bot.edit_message_text(tts, c.message.chat.id, c.message.id, reply_markup=kb,
                          parse_mode="Markdown")


@bot.callback_query_handler(lambda c: c.data.startswith(VIEW_INVITATION_CALLBACK))
def invitation_approve(c: types.CallbackQuery):
    invitation_id = int(c.data.split(' ', 1)[1])
    invitation = db.get_invitation(invitation_id)

    if not invitation:
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Запрошення №{invitation_id} вже загубили.", c.message.chat.id, c.message.id)
        return

    i_view = InvitationView(invitation)
    kb = i_view.get_keyboard()

    if not i_view.house:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(
            text=f"🔙Назад", callback_data=INVITATION_LIST_CALLBACK
        ))
        bot.answer_callback_query(c.id, "🤕Ойойой...", show_alert=False)
        bot.edit_message_text(f"🤕Дім з запрошення №{invitation_id} вже знесли.",
                              c.message.chat.id, c.message.id, reply_markup=kb)
        return

    kb.add(types.InlineKeyboardButton(
        text=f"🔙Назад", callback_data=INVITATION_LIST_CALLBACK
    ))

    bot.edit_message_text(i_view.get_text(), c.message.chat.id, c.message.id, reply_markup=kb,
                          parse_mode="Markdown")

