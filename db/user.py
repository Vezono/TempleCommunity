from mongoengine import Document, StringField, IntField

from db.house import House


class User(Document):
    id = IntField(primary_key=True)
    name = StringField(default='Unknown')
    money = IntField(default=0)

    status = StringField(default='goi')

    partner = IntField(default=0)
    house = StringField(default="")

    def profile(self):
        tts = (f"*👤Профіль громадянина Храму*: \n"
               f"🆔ID: `{self.id}`\n"
               f"📝Ім'я: `{self.name}`\n"
               f"🛂Статус: {self.get_status()}\n"
               f"🧧Баланс: {self.money}\n"
               f"\n"
               f"💞Партнер: {self.get_partner_name()}\n"
               f"🏘Дім: {self.get_house_name()}")
        return tts

    def get_house_name(self):
        if self.house == "":
            return "відсутній"
        else:
            return House.objects.get(id=self.house).name

    def get_status(self):
        if self.status == 'goi':
            return "гой"
        elif self.status == 'jew':
            return "єврей"
        else:
            return "невідомий"

    def get_partner_name(self):
        if self.partner == 0:
            return 'відсутній'
        else:
            return User.objects.get(id=self.partner).name
