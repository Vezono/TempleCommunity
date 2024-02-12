
class ApprovalFlowInvitationStrategy(ApprovalFlowStrategy):
    def __init__(self, approval_flow: ApprovalFlow):
        super().__init__()

    def init(context: Context) -> BasicResultValueObject:


    def complete(context: Context):
        # Here invitation complete logic
        if context.message.reply_to_message:
            tg_user = context.message.reply_to_message.from_user
        else:
            return BasicResultValueObject("🤕І шо ви робите мені нєрви по пустяках?", false)
        goi = db.get_user(tg_user.id)
        user = db.get_user(m.from_user.id)
        house = db.get_house(user.house)

        if goi.id == user.id:
            return BasicResultValueObject("🤯Геній?")
        if not house:
            return BasicResultValueObject("👮В вас нема дому! Куди запрошувать?")
        if user.status == 'goi':
            return BasicResultValueObject( "🤕Ви гой, і Махновщину ще не побудували.")


        for existing_approval_flow in db.get_approval_flows(goi_id=goi.id):
            if existing_approval_flow.house_id == house.id:
                approval_flow = existing_approval_flow
                break

        if not invitation:
            approval_flow = db.create_approval_flow(goi_id=goi.id, house_id=house.id)
        
        return approval_flow