from configparser import ConfigParser
from os.path import join, dirname, realpath
import socket

class Config:

    # 初始化
    def __init__(self, route=""):
        self.__config = ConfigParser()
        self.__config.read(join(route, 'config.ini'), encoding = 'utf8')
        self.__value = ''

    # 取用「設定檔」內資料庫參數
    def getDatabase(self):
        data = {
            "host": self.getIPAddress(),
            "port": int(self.__config["database"]["port"]),
            "user": str(self.__config["database"]["user"]),
            "passwd": str(self.__config["database"]["password"]),
            "db": str(self.__config["database"]["database"]),
            "charset": str(self.__config["database"]["charset"]),
        }

        return data

    # 取用「設定檔」一般 section 的 key 之 value
    def getValue(self, section, key):
        self.value = self.__config[section][key]
        return self.value

    def getWebSocketUrl(self):
        ws = 'http://' + self.getIPAddress() + ':' + self.getValue('host', 'port')
        return ws

    @staticmethod
    def getIPAddress():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip
