from os.path import join, dirname, realpath, pardir, abspath
import time, jwt, sys

class Key():
    
    def __init__(self):
        # 取得根目錄
        self.__ROOT_DIR = abspath(join(dirname(realpath(__file__)), pardir, pardir))

        # 讀取「RSA-2048」金鑰
        self.__PUBLIC_KEY_FILE = open(join(self.__ROOT_DIR, 'key/public.pem'), 'r', encoding='UTF-8')
        self.__PUBLIC_KEY = self.__PUBLIC_KEY_FILE.read()
        self.__PRIVATE_KEY_FILE = open(join(self.__ROOT_DIR, 'key/private.pem'), 'r', encoding='UTF-8')
        self.__PRIVATE_KEY = self.__PRIVATE_KEY_FILE.read()

    def getPublicKey(self):
        return self.__PUBLIC_KEY
    
    def getPrivateKey(self):
        return self.__PRIVATE_KEY
