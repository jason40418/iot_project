from __main__ import socketio
from flask_socketio import send, emit

@socketio.on('connect')
def connect():
    print('YES CALL ME')
    emit('connect', {'data': 'Connected'}, json=True)

def ack():
    print('message was received!')

@socketio.on('test')
def test(data):
    print("HELLO")
    json = {
        'test': "received"
    }
    emit('test', json, json=True, callback=ack)
    emit('test', json, json=True, broadcast=True)

@socketio.on('front-end-publish')
def monitor(data):
    json = {
        'yes': 'succcess'
    }
    print(json)
    emit('server_receive', {'receive': True}, json=True)
    emit('front-end-response', json, json=True, broadcast=True)