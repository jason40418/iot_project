import bcrypt
from datetime import datetime
from model.util.Overload import MultipleMeta

class Member(metaclass=MultipleMeta):

    def __init__(self, account: str, name: str, email: str, password: str, identity: str):
        '''
        <Constructor> 用於新增會員
        '''
        self.__id = -1
        self.__account = account
        self.__name = name
        self.__email = email
        self.__password = self.__encrypt_password(password)
        self.__identity = identity
        self.__create = datetime.now().replace(microsecond=0)
        self.__modify = datetime.now().replace(microsecond=0)

    def __init__(self, id: int, account: str, name: str, email: str, password: str, identity: str, create: datetime, modify: datetime):
        '''
        <Constructor> 用於新增會員
        '''
        self.__id = id
        self.__account = account
        self.__name = name
        self.__email = email
        self.__password = password
        self.__identity = identity
        self.__create = create
        self.__modify = modify

    def set_account_id(self, id):
        self.__id = id

    def update(self, name, email, password):
        self.__name = name
        self.__email = email
        self.__password = self.__encrypt_password(password)
        self.__modify = datetime.now().replace(microsecond=0)

    def get_all_parameter(self):
        return {
            'id'       : self.__id,
            'account'  : self.__account,
            'name'     : self.__name,
            'email'    : self.__email,
            'password' : self.__password,
            'identity' : self.__identity,
            'create'   : self.__create,
            'modify'   : self.__modify
        }

    def __encrypt_password(self, passwd):
        # 加密密碼
        encoded_password = passwd.encode("utf-8")
        hash_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
        return hash_password
