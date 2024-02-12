from core.controller import Controller
from core.router import router
from constants import *
from core.context import Context
from views.tora_view import ToraView
from views.tora_basic_item_view import ToraBasicItemView


class FinanceController(Controller):
    def __init__(self):
        super().__init__()

    @router.register_command('tora')
    def tora(context: Context):
        return ToraView()

    @router.register_callback(MAIN_HELP_CALLBACK)
    def chat_rules_callback(context: Context):
        return ToraBasicItemView(
            "Верховна Жриця тримає правила <a href='https://t.me/c/1958799638/106716'>ось тут</a>. Почитайте.")

