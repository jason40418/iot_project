from model.util.Overload import MultipleMeta

class MemberPrference(metaclass=MultipleMeta):

    def __init__(self, account: str, item: str, min_value: float, max_value: float):
        '''
        <Constructor>
        '''
        self.__id = -1
        self.__account = account
        self.__item = item
        self.__min_value = min_value
        self.__max_value = max_value

    def __init__(self, id: int, account: str, item: str, min_value: float, max_value: float):
        '''
        <Constructor>
        '''
        self.__id = id
        self.__account = account
        self.__item = item
        self.__min_value = min_value
        self.__max_value = max_value

    def set_id(self, id):
        self.__id = id

    def update(self, name, email, password):
        self.__name = name
        self.__email = email
        self.__password = self.__encrypt_password(password)
        self.__modify = datetime.now().replace(microsecond=0)

    def get_all_parameter(self):
        return {
            'id'        : self.__id,
            'account'   : self.__account,
            'item'      : self.__item,
            'min'       : self.__min_value,
            'max'       : self.__max_value
        }
