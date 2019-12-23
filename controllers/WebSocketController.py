from __main__ import socketio
import datetime
from flask import jsonify, request
from flask_socketio import send, emit
from model.helper.AccessHelper import AccessHelper

@socketio.on('connect', namespace='/exit')
def exit_connect():
    client_id = request.sid
    print('[@WebScoketController] Manage exit camaera {} connect!'.format(client_id))
    emit('connect', {'id': client_id}, namespace='/system', json=True)

@socketio.on('disconnect', namespace='/exit')
def exit_disconnect():
    client_id = request.sid
    print('[@WebScoketController] Manage exit camaera {} disconnect!'.format(client_id))
    emit('disconnect', {'id': client_id}, namespace='/system', json=True)

@socketio.on('connect', namespace='/system')
def system_connect():
    client_id = request.sid
    print('[@WebScoketController] A new user {} connect to system room!'.format(client_id))
    emit('connect', {'id': client_id}, namespace='/system', json=True)

@socketio.on('disconnect', namespace='/system')
def system_disconnect():
    client_id = request.sid
    print('[@WebScoketController] Client {} disconnect to system room!'.format(client_id))
    emit('disconnect', {'id': client_id}, namespace='/system', json=True)

@socketio.on('connect', namespace='/client')
def client_connect():
    client_id = request.sid
    print('[@WebScoketController] A new user {} connect!'.format(client_id))
    emit('connect', {'id': client_id}, namespace='/client', json=True)

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    client_id = request.sid
    print('[@WebScoketController] Client {} disconnect!'.format(client_id))
    emit('disconnect', {'id': client_id}, namespace='/client', json=True)

# ==================================================================================================
# Raspberry Pi and Server
# ==================================================================================================
@socketio.on('connect', namespace='/pi')
def pi_connect():
    client_id = request.sid
    print('[@WebScoketController] Pi System {} connect!'.format(client_id))
    emit('connect', {'id': client_id}, namespace='/pi', json=True)

@socketio.on('disconnect', namespace='/pi')
def pi_disconnect():
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
    emit('sensor_data_pub_system', data, namespace='/system', json=True, broadcast=True)

    return True, "receive", 200

# 處理人員進入環境
@socketio.on('face_identify_pub_pi', namespace='/pi')
def face_identify_pub_pi(payload):
    dt = datetime.datetime.today()
    result = payload
    vaild = list()

    for person in payload['data']['people']:
        exist, record = AccessHelper.get_by_name(person)
        if not exist:
            vaild.append(person)
            AccessHelper.entry(person)
        elif record['datetime'].day < dt.day:
            vaild.append(person)
            AccessHelper.exit(person, record['datetime'], 'system')
            AccessHelper.entry(person)
        else:
            pass

    # 將最終判別結果告知前端
    result['data']['people'] = vaild
    emit('face_identify_pub_system', result, namespace='/system', json=True, broadcast=True)
    # 提醒前端使用者有新的照片可以更新了
    emit('face_identify_pub_client', result, namespace='/client', json=True, broadcast=True)

    return True, "receive", 200

# 處理人員離開環境（假設一定要有進入才有出去）
@socketio.on('face_identify_pub_pi', namespace='/exit')
def face_identify_exit_pub_pi(payload):
    dt = datetime.datetime.today()
    result = payload
    vaild = list()

    for person in payload['data']['people']:
        exist, record = AccessHelper.get_by_name(person)
        if exist:
            vaild.append(person)
            AccessHelper.exit(person, record['datetime'], None)
        else:
            pass

    # 將最終判別結果告知前端
    result['data']['people'] = vaild
    emit('face_identify_pub_system', result, namespace='/system', json=True, broadcast=True)
    # 提醒前端使用者有新的照片可以更新了
    emit('face_identify_pub_client', result, namespace='/client', json=True, broadcast=True)

    return True, "receive", 200

# ==================================================================================================
# Test
# ==================================================================================================
def ack():
    print('message was received!')
