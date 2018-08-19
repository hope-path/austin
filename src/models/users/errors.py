class UserNotExistsError(Exception):
    def __init__(self,message):
        self.message = message
class IncorrectPassword(Exception):
    def __init__(self,message):
        self.message = message
class UserExists(Exception):
    def __init__(self,message):
        self.message = message
class Invalid_email(Exception):
    def __init__(self,message):
        self.message = message