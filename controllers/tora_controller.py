# цей файл створив КОЗІЧ (я тут нідочого)
from core.controller import Controller
from core.router import router
from constants import *
from core.context import Context
from views.tora_view import ToraView
from views.tora_basic_item_view import ToraBasicItemView


class ToraController(Controller):
    def __init__(self):
        pass

    @router.register_command('tora')
    def tora(context: Context):
        return ToraView()

    @router.register_callback(MAIN_HELP_CALLBACK)
    def main(context: Context):
        return ToraView()

    @router.register_callback(CHAT_RULES_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(
            "Верховна Жриця тримає правила <a href='https://t.me/c/1958799638/106716'>ось тут</a>. Почитайте.",
            "HTML")

    @router.register_callback(ROLE_HELP_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(("🏅У деяких олдфагів Храму установились соціальні ролі. Це *Дев'ятка*.\n\n"

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
                                  ))

    @router.register_callback(WHY_HELP_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(
            ("- Чому я ще не можу додавати гоїв? Робити щось з домом? Чому все за мене робить Юрист?\n"
             "- Тому що Варта ще не готова. Почекайте трохи.\n\n"
             "- Звідки будуть братись гроші?\n"
             "- Усі члени дому будуть заробляти по формулі. Також можна заробляти на ставках з битви гоїв "
             "і за продаж Предметів.\n\n"
             "- В мене було дофіга гоїв. Де вони всі?\n"
             "- Гої зі старого реєстру аннулюються. Гої до вашого дому повинні вступити знову. Вербуйте.\n\n"
             "- Нафіга цей бот взагалі? Він не потрібен\n"
             "- <tg-spoiler>Іді нахуй</tg-spoiler>"))

    @router.register_callback(COMMANDS_HELP_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(("💻Список команд Варти:\n\n"
                                  "/tora - почитати Тору.\n"
                                  "/profile - паспорт громадянина Храму.\n"
                                  "/registry - реєстр домів Храму.\n"
                                  "/house - інформація про ваш дім.\n"
                                  "/found - заснувати дім. Не забудьте надати ім'я.\n"))

    @router.register_callback(HOUSE_HELP_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(
            ("🏡Доми - це такі об'єднання жидів та гоїв у міні-фракції, або групки. Дім може створити будь-хто. "
             "Стати членом можна тільки з повної згоди вступаючого та повного консенсусу голів дому. "
             "За дотримуванням згоди слідкує Юрист.\n\n"
             "Нових голів назначають консенсусом поточних голів дому. Конфлікти під час прибирання голів допомагає "
             "вирішуватти Суддя або Верховна Жриця."))

    @router.register_callback(JEWISH_HELP_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(
            ("✡️Жиди - це зазвичай олдфаги чату. Ми любимо євреїв, вони прикольні. Слово жид у нас навпаки "
             "суспільній думці обозначає високий стан у суспільстві.\n"
             "🤷Гої - не євреї. Зазвичай це новачки або люди які не пройшли стажування в єврейських домах. "
             "Це не обов'язково погані люди.\n"
             "☪️Невірні гої, або нижчі гої - люди які займаються гойством. Гойство - це щось дурне, "
             "некультурне або неприйнятне. Ми тут таких не любимо.\n"))
