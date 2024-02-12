
class ResultValueObject<T>:
    def __init__(self, message: str, is_success: bool, value: T):
        self.message = message
        self.is_success = is_success
        self.value = value

class BasicResultValueObject(ResultValueObject<None>):
    def __init__(self, message: str, is_success: bool):
        super.__init__(message, is_success, None)
