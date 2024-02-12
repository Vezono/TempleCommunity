# цей файл створив КОЗІЧ (я тут нідочого)
from core.controller import Controller
from core.router import router
from constants import *
from core.context import Context
from views.invitations_view import InvitationsView
from views.invintation_view import InvintationView
from views.tora_basic_item_view import ToraBasicItemView
from views.basic_text_view import BasicTextView
from db.invitation import Invitation
from db.invitation_participant import InvitationParticipant
from model.approval_flow.approval_flow_factory import ApprovalFlowFactory

from db import db

class ApprovalFlowController(Controller):
    def __init__(self):
        super().__init__()

    
    @router.register_commands(['invite'])
    def invite_handler(context: Context):
    
        approval_flow_factory = ApprovalFlowFactory()

        approval_flow_strategy = approval_flow_factory.get("invitation")
        
        result = approval_flow_factory.init(context)

        if (result)
        if context.message.reply_to_message:
            tg_user = context.message.reply_to_message.from_user
        else:
            return BasicTextView("🤕І шо ви робите мені нєрви по пустяках?")

        goi = db.get_user(tg_user.id)
        user = db.get_user(m.from_user.id)
        house = db.get_house(user.house)

        if goi.id == user.id:
            return BasicTextView("🤯Геній?")
        if not house:
            return BasicTextView("👮В вас нема дому! Куди запрошувать?")
        if user.status == 'goi':
            return BasicTextView( "🤕Ви гой, і Махновщину ще не побудували.")


        for existing_invitation in db.get_invitations(goi_id=goi.id):
            if existing_invitation.house_id == house.id:
                invitation = existing_invitation
                break

        if not invitation:
            invitation = db.create_invitation(goi_id=goi.id, house_id=house.id)

        return InvitationView(invitation)
    
    @router.register_command('invites')
    def invites_handler(context: Context):
        return InvintationsView()

