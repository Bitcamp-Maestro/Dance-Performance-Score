
from server.settings import DB
from datetime import datetime
import pytz
KST = pytz.timezone('Asia/Seoul')


class User(object):
    def __init__(self, name, password, join_date='', email='', faves_list=[], views_list=[] ):
        self.name = name
        self.password= password
        self.join_date = datetime.now(KST) if join_date == '' else join_date
        self.email = email
        self.faves_list = faves_list
        self.views_list = views_list

    @staticmethod
    def isExists(name):
        doc = DB.collection(u'User').where(u'name', u'==', name).get()
        if len(doc) == 1:
            return doc[0]
        else:
            return None

    @staticmethod
    def Login(name, password):
        users = DB.collection(u'User').where(u'name', u'==', name).stream()
        print(users)
        for user in users:
            print(user)
        return users

    @staticmethod
    def from_dict(source):
        pass

    def to_dict(self):
        return self.__dict__

    def __repr__(self) -> str:
        return super().__repr__()