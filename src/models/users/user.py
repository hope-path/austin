import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as Usererror
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User{}>".format(self.email)




    def is_login_valid(email, password):
        user_data = Database.find_one("users", {"email": email})
        if user_data is None:
               raise Usererror.UserNotExistsError("user is not valid")
        if not Utils.check_hashed_password(password, user_data['password']):
                raise Usererror.IncorrectPassword("incorrect password")

        return True

    def registeruser(email,password):
        user_data = Database.find_one('users', {"email": email})
        if user_data is None:
            if Utils.email_is_valid(email):
                data =User(email, Utils.hash_password(password))
                data.Save_to_mongo()
                return True
            raise Usererror.Invalid_email("The email was not in correct format")
        raise Usererror.UserExists("USER already exists")

    def Save_to_mongo(self):
       Database.insert("users", self.json())


    def json(self):
       return {
        'email': self.email,
        'password': self.password,
        '_id': self._id
    }


    @classmethod
    def find_by_email(cls,email):
        return cls(**Database.find_one('users',{'email':email}))

    def get_alerts(self):
        return Alert.find_alert_by_email(self.email)
