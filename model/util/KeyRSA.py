from Crypto.PublicKey import RSA
from model.util.Overload import MultipleMeta
from model.util.Config import Config

class KeyRSA(metaclass=MultipleMeta):

    def __init__(self, bits:int=-1):
        # 產生RSA金鑰位元數量
        # TODO: 應該檢查金鑰bits數量
        self.__cfg = Config()
        self.__bits = bits if bits > 0 else int(self.__cfg.getValue('RSA', 'bits'))
        self.__key_pair = RSA.generate(self.__bits)
        self.__public_key = self.__key_pair.publickey().exportKey().decode()
        self.__private_key = self.__key_pair.exportKey().decode()
        del self.__key_pair

    def __init__(self, public_key:str, private_key:str, bits:str):
        self.__bits = bits
        self.__public_key = public_key
        self.__private_key = private_key

    def get_private_key(self):
        return self.__private_key

    def get_public_key(self):
        return self.__public_key

    def get_bits(self):
        return self.__bits
