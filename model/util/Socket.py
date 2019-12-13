import socketio
from model.util.Config import Config

class Socket():

    def __init__(self, namespaces=['/', '/pi'], transports='websocket'):
        self.__namespace = namespaces
        self.__transports = transports
        self.__config = Config()
        self.__ip = self.__config.getIPAddress()
        self.__port = self.__config.getValue('host', 'port')
        self.__socket = None
        self.__connected = False

    def get_socket(self):
        return self.__socket

    def connect(self):
        ws = self.__config.getWebSocketUrl()
        self.__socket = socketio.Client()

        if not self.__connected:
            try:
                self.__socket.connect(ws, namespaces=self.__namespace, transports=self.__transports)
            except socketio.exceptions.ConnectionError as err:
                print("[@Socket] Connection Socket Error: {}".format(err))
            else:
                self.__connected = True

        return self.__connected

    def close(self):
        if self.__connected:
            self.__socket.disconnect()
            self.__connected = False
