import typing
import uuid
from typing import Optional

from mongoengine import connect
from config import mongourl
from db.house import House
from db.invitation import Invitation
from db.invitation_participant import InvitationParticipant
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

    def get_invitation(self, invitation_id: int) -> Optional[Invitation]:
        try:
            return Invitation.objects.get(id=invitation_id)
        except:
            pass

    def create_house(self, house_id: str, name: str):
        house = House(id=house_id, name=name)
        house.save()
        return house

    def create_invitation(self, goi_id: int, house_id: str):
        jews = list(self.get_jews(house_id))
        participants = []
        invitation = Invitation(goi_id=goi_id, house_id=house_id)
        for jew in jews:
            participant = InvitationParticipant(user=jew, invitation_id=invitation.id)
            participant.save()
            participants.append(participant)
        invitation.participants = participants
        invitation.save()
        return invitation

    def get_invitations(self, goi_id: int) -> typing.Iterable[Invitation]:
        for invitation in Invitation.objects(goi_id=goi_id):
            yield invitation

    def get_jews(self, house_id: str):
        for user in User.objects(house=house_id):
            if user.status == 'jew':
                yield user

    def get_gois(self, house_id: str):
        for user in User.objects(house=house_id):
            if user.status == 'goi':
                yield user
