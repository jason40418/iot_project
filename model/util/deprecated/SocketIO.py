from threading import Timer, Event, Thread

import json
import websocket


class SocketIO(Thread):
    def __init__(self, debug=False):
        super(SocketIO, self).__init__()
        websocket.enableTrace(True)
        self.__ws = websocket.WebSocketApp("ws://192.168.1.111:3000/socket.io/?EIO=3&transport=polling")

        if debug: self.__debug()

    def getConnection(self):
        return self.__ws

    def __debug(self):
        def on_message(ws, message):
            print(message)

        def on_error(ws, error):
            print(error)


        def on_close(ws):
            print("### closed ###")

        def on_open(ws):
            self.__ws.send("2probe")
        
        self.__ws.on_message = on_message
        self.__ws.on_error = on_error
        self.__ws.on_close = on_close
        self.__ws.on_open = on_open

    def sendPing(self):
        self.ws.send('2')
    
    def sendMsg(self, channel, payload):
        def on_emit(ws, channel, payload):
            # 发送信息
            # 4: engine.io message
            # 2: socket.io event
            # chat message event message
            ws.send('42["{0}","{1}"]'.format(channel, payload))

        t = Timer(3, on_emit, args=(self.__ws, channel, payload,))
        t.start()
        self.__ws.run_forever()