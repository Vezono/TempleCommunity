from model.approval_flow.approval_flow import ApprovalFlow
from core.context import Context
from core.result_value_object import ResultValueObject

class ApprovalFlowStrategy:
   def __init__(self, approval_flow: ApprovalFlow):
         self.approval_flow = approval_flow


    def init(context: Context) -> BasicResultValueObject:
        pass        

    def complete(context: Context):
        pass


class ApprovalFlowPromotionStrategy(ApprovalFlowStrategy):
    def __init__(self, approval_flow: ApprovalFlow):
        super().__init__()

    def init(context: Context) -> BasicResultValueObject:

    def complete(context: Context):
        # Here promotion complete logic

class ApprovalFlowFactory:
    def __init__(self):
        super().__init__()

    def get(vote_type: str): ApprovalFlowStrategy:
        if vote_type == "invitation":
            return ApprovalFlowInvitationStrategy()
        if vote_type == "promotion":
            return ApprovalFlowPromotionStrategy()
