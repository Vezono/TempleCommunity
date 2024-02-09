from mongoengine import Document, StringField, ReferenceField, IntField

from db.user import User


class InvitationParticipant(Document):
    user = ReferenceField(User)
    invitation_id = IntField()
    status = StringField()


