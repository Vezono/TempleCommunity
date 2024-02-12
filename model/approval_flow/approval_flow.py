from typing import Iterable

from mongoengine import Document, StringField, IntField, ListField, SequenceField, BinaryField
from .approval_flow_actor import ApprovalFlowActor


class ApprovalFlow(Document):
    id = SequenceField(primary_key=True, collection_name="approval_flow_sequencer")
    vote_type = StringField()

    initiator_user_id = IntField()
    house_id = StringField()
    subject_label = StringField()
    subject_id = StringField()
    required_percentage = IntField()

    actors = ListField()
    status = StringField(default="pending")

    @property
    def ready(self):
        required_count = self.required_percentage / (100 / len(self.actors))
        if len(self.approved) >= required_count:
            return True
        return False

    def get_actor(self, user_id: int):
        for actor in self.actors:
            actor: ApprovalFlowActor
            if actor.user.id == user_id:
                return actor

    @property
    def approved(self) -> Iterable[ApprovalFlowActor]:
        for actor in self.actors:
            actor: ApprovalFlowActor
            if actor.status == 'approved':
                yield actor

    @property
    def pending(self) -> Iterable[ApprovalFlowActor]:
        for actor in self.actors:
            actor: ApprovalFlowActor
            if actor.status == 'pending' or not actor.status:
                yield actor

    @property
    def rejected(self) -> Iterable[ApprovalFlowActor]:
        for actor in self.actors:
            actor: ApprovalFlowActor
            if actor.status == 'rejected':
                yield actor
