import time, jwt
from os.path import join, dirname, realpath, pardir, abspath
from model.util import *

class Auth():

    def __init__(self):
        # 取得根目錄
        self.__ROOT_DIR = abspath(join(dirname(realpath(__file__)), pardir))
        self.__config = Config.Config(self.__ROOT_DIR)

        # 取得設定檔內token有效的時間長度
        self.__EXPIRED_LENGTH = float(self.__config.getValue('account', 'expire'))
        self.__key = Key.Key()
        self.__PUBLIC_KEY = self.__key.getPublicKey()
        self.__PRIVATE_KEY = self.__key.getPrivateKey()

    def __encode(self, payload):
        token = jwt.encode(payload, self.__PRIVATE_KEY, algorithm='RS512')
        return token
    
    def __decode(self, token):
        if token is None:
            return False
        try:
            payload = jwt.decode(token, self.__PUBLIC_KEY, algorithms=['RS512'])
            return payload
        # decode error or expired
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False

    def get_token(self, **kwargs):
        expire_time = time.time() + self.__EXPIRED_LENGTH
        payload = {
            'expire': expire_time
        }
        payload.update(kwargs)
        print(payload)
        token = self.__encode(payload)
        return token
