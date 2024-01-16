from mongoengine import Document, StringField, IntField, ListField


class House(Document):
    id = StringField(primary_key=True)
    name = StringField(required=True)
    description = StringField(default="Якийсь Дім жидів. Головні жиди цього дому повинні додати сюди якусь "
                                      "інформацію - девіз, слоган, або просто опис.")

    money = IntField(default=0)
    founders = ListField()
    ratio = IntField(default=70)
