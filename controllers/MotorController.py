import subprocess, time
import RPi.GPIO as GPIO
from flask import Blueprint, jsonify, render_template, request
from __main__ import app, socketio
from model.util import Config as cfg
from model.util.General import get_accessory_publish_data
from flask_socketio import send, emit

# 取得設定檔案
root_dir = app.root_path
config = cfg.Config(root_dir)

# 定義
motor_blueprint = Blueprint('motor', __name__)
motor_status = False
pin_num = config.getValue('motor', 'pin')
pin_mode = config.getValue('motor', 'mode')

def check_motor_status():
    global motor_status
    socketio.emit('motor_status_check_pub_system', {'action': 'check'}, json=True, broadcast=True, namespace='/pi')
    time.sleep(.5)

@socketio.on('motor_status_pub_pi', namespace='/pi')
def bread_motor_status(data):
    global motor_status
    motor_status = data['status']
    # 將目前狀態發布給Client端（結束也會主動發布給Server）
    emit_data = get_accessory_publish_data('motor', motor_status)
    socketio.emit('accessory_status_pub_client', emit_data, json=True, broadcast=True, namespace='/client')

@motor_blueprint.route("/on")
def main():
   global motor_status
   global pin_num
   global pin_mode

   # 判斷伺服馬達是否已經打開
   if not motor_status:
      proc = subprocess.Popen(["python3 Motor.py"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)
      # TODO: 檢查元件已經正確被開啟
      motor_status = True
      return jsonify({
         'pin'      : pin_num,
         'mode'     : pin_mode,
         'accessory': 'motor',
         'status'   : motor_status,
         'code'     : 200,
         'type'     : 'MotorCloseSuccess',
         'msg'      : '伺服馬達已經開啟！'
      }), 200
   else:
      return jsonify({
         'pin'        : pin_num,
         'mode'       : pin_mode,
         'accessory'  : 'motor',
         'status'     : motor_status,
         'error_code' : 400,
         'error_type' : 'MotorReopen',
         'error_msg'  : '請勿重複開啟伺服馬達！'
      }), 400

@motor_blueprint.route("/off")
def off_led():
   global motor_status
   global pin_num
   global pin_mode
   # 判斷伺服馬達是否已經打開
   if motor_status:
      # TODO: 檢查元件已經正確被關閉
      motor_status = False
      data = {
         'pin'      : pin_num,
         'mode'     : pin_mode,
         'code'     : 200,
         'accessory': 'motor',
         'status'   : motor_status,
         'type'     : 'MotorCloseSuccess',
         'msg'      : '伺服馬達已經關閉！'
      }
      socketio.emit('motor_off_publish_server', data, json=True, namespace='/pi', broadcast=True)
      return jsonify(data), 200
   else:
      return jsonify({
         'pin'       : pin_num,
         'mode'      : pin_mode,
         'accessory' : 'motor',
         'status'    : motor_status,
         'error_code': 400,
         'error_type': 'MotorUnopen',
         'error_msg' : '請勿在未開啟狀態關閉伺服馬達！！'
      }), 400

   return jsonify(data), 400
