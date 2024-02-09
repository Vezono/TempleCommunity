from typing import Iterable

from mongoengine import Document, StringField, IntField, ListField, SequenceField, BinaryField
from .invitation_participant import InvitationParticipant


class Invitation(Document):
    id = SequenceField(primary_key=True, collection_name="invitation_sequencer")
    goi_id = IntField()
    house_id = StringField()

    participants = ListField()

    status = StringField(default="pending")

    @property
    def ready(self):
        if not list(self.pending) and not list(self.rejected) and self.status == "accepted":
            return True
        return False

    def get_participant(self, user_id: int):
        for participant in self.participants:
            participant: InvitationParticipant
            if participant.user.id == user_id:
                return participant

    @property
    def approved(self) -> Iterable[InvitationParticipant]:
        for participant in self.participants:
            participant: InvitationParticipant
            if participant.status == 'approved':
                yield participant

    @property
    def pending(self) -> Iterable[InvitationParticipant]:
        for participant in self.participants:
            participant: InvitationParticipant
            if participant.status == 'pending' or not participant.status:
                yield participant

    @property
    def rejected(self) -> Iterable[InvitationParticipant]:
        for participant in self.participants:
            participant: InvitationParticipant
            if participant.status == 'rejected':
                yield participant
