import uuid

from config import telegram_token, lawyer_id
from telebot import types

from constants import *
from db.house import House
from db import db
from utils import Bot, MatrixIndexPlacer, MatrixIndexCounter
from view import View

bot = Bot(telegram_token)

view = View()


def root_handler(m: types.Message):
    user = db.get_user(m.from_user.id)
    if not user:
        db.create_user(m.from_user.id, m.from_user.full_name)


@bot.message_handler(func=root_handler)
def _(_):
    return


@bot.message_handler(commands=['start'])
def start_handler(m: types.Message):
    root_handler(m)

    bot.respond_to(m, "🫡")


@bot.message_handler(commands=['found'])
def found_handler(m: types.Message):
    root_handler(m)

    if m.text.count(' ') < 1:
        bot.respond_to(m, "🤕І шо?")
        return

    if m.from_user.id != lawyer_id:
        bot.respond_to(m, "🙇‍♀️Сорі, поки шо тільки Юрист може створювати дома. "
                          "Коли бот буде готовий, то усі зможуть.")

    name = m.text.split(" ", 1)[1]

    db.create_house(str(uuid.uuid4()), name)
    bot.respond_to(m, f"🪚Засновано дім \"{name}\".")


@bot.message_handler(commands=['registry'])
def registry_handler(m: types.Message):
    root_handler(m)

    kb = view.house_list_keyboard()
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


@bot.message_handler(commands=['house'])
def house_handler(m: types.Message):
    root_handler(m)
    user = db.get_user(m.from_user.id)

    house = db.get_house(user.house)

    tts = view.house_info_text(house)
    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['house'])
def profile_handler(m: types.Message):
    root_handler(m)
    user = db.get_user(m.from_user.id)

    house = db.get_house(user.house)

    if not house:
        bot.respond_to(m, "👮В вас нема дому!")
        return

    tts = view.house_info_text(house)
    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['profile'])
def profile_handler(m: types.Message):
    root_handler(m)
    user = db.get_user(m.from_user.id)
    tts = user.profile()
    if user.status == 'goi':
        tts += (f"\n\n*Чому ти гой?*\n"
                f"Тому що ти новачок, і не пройшов \"стажування\". "
                f"Стажування проходиться в єврейських домах (/registry).")
    if user.house == '':
        tts += (f"\n\n*Чому ти безхатько?*\n"
                f"Тому що не вступив в дім, або не створив свій!")
    bot.respond_to(m, tts, parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def help_handler(m: types.Message):
    root_handler(m)

    kb, tts = view.tora()
    bot.respond_to(m, tts, reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data.startswith(MAIN_HELP_CALLBACK))
def chat_rules_callback(c: types.CallbackQuery):
    kb, tts = view.tora()
    bot.edit_message_text(tts, c.message.chat.id, c.message.id, reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data.startswith(CHAT_RULES_CALLBACK))
def chat_rules_callback(c: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="↩️Назад до Тори", callback_data=MAIN_HELP_CALLBACK))

    tts = "Верховна Жриця тримає правила <a href='https://t.me/c/1958799638/106716'>ось тут</a>. Почитайте."
    bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="HTML", reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data.startswith(ROLE_HELP_CALLBACK))
def chat_rules_callback(c: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="↩️Назад до Тори", callback_data=MAIN_HELP_CALLBACK))

    tts = ("🏅У деяких олдфагів Храму установились соціальні ролі. Це *Дев'ятка*.\n\n"
           
           "*👸🏻Верховна Жриця:*\n"
           "@ArnaMorno. Власник Сповідальні і голова Храму.\n\n"
           
           "*👩🏻‍⚖️Суддя:*\n"
           "@douxretrouvailles. Має останнє слово під час конфліктів.\n\n"

           "*👨🏻‍💻Юрист:*\n"
           "@gbball. Займається бюрократією та юридичними аспектами Храму. Слідкує за дотримуванням Тори.\n\n"

           "*👮🏻‍♂Інквізитор:*\n"
           "@danylosobko. Відповідає за різню невірних гоїв. Має Зошит Смерті.\n\n"

           "*🤵🏻Економіст:*\n"
           "@Kozoobminnik. Відповідає за економіку, ціни, зарплати та ваші гаманці. Штрафи назначає він.\n\n"

           "*👩🏻‍🎨Військовий:*\n"
           "@venionim. Головує армією. Революціонер. Відповідає за військові дії та тримає актив в Храмі "
           "залізною рукою.\n\n"

           "*🕵🏻Протагоніст:*\n"
           "@Square345. Знає що до чого. Тримає невірних гоїв подалі.\n\n"
           
           "*👩🏻‍✈Варта:*\n"
           "@temple\\_guardiArn\\_bot. Електронний захист вашої безпеки, гаманця та психіки.\n\n"

           "*👁Всевидяче око:*\n"
           "@purgatoriowanderer. Він бачить все. Якщо щось сталось в Храмі - він знатиме.\n\n"
            )

    bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="Markdown", reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data.startswith(HOUSE_HELP_CALLBACK))
def chat_rules_callback(c: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="↩️Назад до Тори", callback_data=MAIN_HELP_CALLBACK))

    tts = ("🏡Доми - це такі об'єднання жидів та гоїв у міні-фракції, або групки. Дім може створити будь-хто. "
           "Стати членом можна тільки з повної згоди вступаючого та повного консенсусу голів дому. "
           "За дотримуванням згоди слідкує Юрист.\n\n"
           "Нових голів назначають консенсусом поточних голів дому. Конфлікти під час прибирання голів допомагає "
           "вирішуватти Суддя або Верховна Жриця.")

    bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="Markdown", reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data.startswith(HOUSE_INFO_CALLBACK))
def house_info_callback(c: types.CallbackQuery):
    house_id = c.data.split('?', 1)[1]

    house = db.get_house(house_id)
    if not house:
        kb = view.house_list_keyboard()
        bot.edit_message_text("🤕Дім не знайдено. Доступні доми надано нижче.", c.message.chat.id, c.message.id,
                              reply_markup=kb)

    tts = view.house_info_text(house)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="↩️Назад до списку домів", callback_data=HOUSE_LIST_CALLBACK))

    bot.edit_message_text(tts, c.message.chat.id, c.message.id, parse_mode="Markdown", reply_markup=kb)


@bot.callback_query_handler(lambda c: c.data.startswith(HOUSE_LIST_CALLBACK))
def house_list_callback(c: types.CallbackQuery):
    buttons = list()
    kb = types.InlineKeyboardMarkup()

    for house in House.objects():
        buttons.append(types.InlineKeyboardButton(text=house.name, callback_data=f"{HOUSE_INFO_CALLBACK}?{house.id}"))

    mip = MatrixIndexPlacer(2)
    matrix = mip.place(buttons)

    for row in matrix:
        kb.add(*row)

    bot.edit_message_text(f"🏘Існуючі доми:", c.message.chat.id, c.message.id, reply_markup=kb)


print("Храмова система запущена. Успішного прогрівання.")
bot.polling()
