from typing import Optional

from mongoengine import connect
from config import mongourl
from db.house import House
from db.user import User


class Database:
    def __init__(self):
        connect(host=mongourl, db='temple')

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except:
            pass

    def create_user(self, user_id: int, name: str):
        user = User(id=user_id, name=name)
        user.save()
        return user

    def get_house(self, house_id: str) -> Optional[House]:
        try:
            return House.objects.get(id=house_id)
        except:
            pass

    def create_house(self, house_id: str, name: str):
        house = House(id=house_id, name=name)
        house.save()
        return house

    def get_jews(self, house_id: str):
        for user in User.objects(house=house_id):
            if user.status == 'jew':
                yield user

    def get_gois(self, house_id: str):
        for user in User.objects(house=house_id):
            if user.status == 'goi':
                yield user
