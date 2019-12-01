import socketio

sio = socketio.Client()
sio.connect('http://192.168.1.111:3000')

@sio.on('server_receive')
def on_message(data):
    print(data)
    sio.disconnect()

sio.emit('front-end-publish', {'foo': 'bar'})
