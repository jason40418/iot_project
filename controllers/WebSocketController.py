from __main__ import socketio
from flask import jsonify, request
from flask_socketio import send, emit


@socketio.on('connect', namespace='/client')
def connect():
    client_id = request.sid
    print('[@WebScoketController] A new user {} connect!'.format(client_id))
    emit('connect', {'id': client_id}, namespace='/client', json=True)

# ==================================================================================================
# Raspberry Pi and Server
# ==================================================================================================
@socketio.on('connect', namespace='/pi')
def connect():
    client_id = request.sid
    print('[@WebScoketController] Pi System {} connect!'.format(client_id))
    emit('connect', {'id': client_id}, namespace='/pi', json=True)

@socketio.on('disconnect', namespace='/pi')
def disconnect():
    client_id = request.sid
    print('[@WebScoketController] Pi System {} disconnect!'.format(client_id))
    emit('disconnect', {'id': client_id}, namespace='/pi', json=True)

@socketio.on('sensor_data_pub_pi', namespace='/pi')
def sensor_data_pub_pi(data):
    """Send the sensor data to client

    Arguments:
        data {[dict]} -- JSON format data the could be emited to client
    """
    emit('sensor_data_pub_client', data, namespace='/client', json=True, broadcast=True)
    return True, "receive", 200

# TODO: 處理人員進出環境
@socketio.on('face_identify_pub_pi', namespace='/pi')
def face_identify_pub_pi(data):
    print("Flask收到了：", data)
    return True, "receive", 200

# ==================================================================================================
# Test
# ==================================================================================================
def ack():
    print('message was received!')
