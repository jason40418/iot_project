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
    emit('front-end-publish', json, json=True, broadcast=True)