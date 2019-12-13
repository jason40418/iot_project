from __main__ import socketio
from flask import jsonify
from flask_socketio import send, emit


@socketio.on('connect')
def connect():
    print('YES CALL ME')
    emit('connect', {'data': 'Connected'}, json=True)

# ==================================================================================================
# Raspberry Pi and Server
# ==================================================================================================
@socketio.on('connect', namespace='/pi')
def connect():
    print('YES CALL ME')
    emit('connect', {'data': 'Connected'}, json=True)

@socketio.on('sensor_data_pub_pi', namespace='/pi')
def sensor_data_pub_pi(data):
    """Send the sensor data to client

    Arguments:
        data {[dict]} -- JSON format data the could be emited to client
    """
    emit('sensor_data_pub_client', data, namespace='/client', json=True, broadcast=True)
    return True, "receive", 200

# ==================================================================================================
# Test
# ==================================================================================================
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
