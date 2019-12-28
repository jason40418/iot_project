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
buzzer_blueprint = Blueprint('buzzer', __name__)
buzzer_status = False
pin_num = config.getValue('buzzer', 'pin')
pin_mode = config.getValue('buzzer', 'mode')

def check_buzzer_status():
    global buzzer_status
    socketio.emit('buzzer_status_check_pub_system', {'action': 'check'}, json=True, broadcast=True, namespace='/pi')
    time.sleep(.5)

@socketio.on('buzzer_status_pub_pi', namespace='/pi')
def bread_buzzer_status(data):
    global buzzer_status
    buzzer_status = data['status']
    # 將目前狀態發布給Client端（結束也會主動發布給Server）
    emit_data = get_accessory_publish_data('buzzer', buzzer_status)
    socketio.emit('accessory_status_pub_client', emit_data, json=True, broadcast=True, namespace='/client')

@buzzer_blueprint.route("/on")
def main():
   global buzzer_status
   global pin_num
   global pin_mode

   # 判斷蜂鳴器是否已經打開
   if not buzzer_status:
      proc = subprocess.Popen(["python3 Buzzer.py"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)
      # TODO: 檢查元件已經正確被開啟
      buzzer_status = True
      return jsonify({
         'pin'      : pin_num,
         'mode'     : pin_mode,
         'accessory': 'buzzer',
         'status'   : buzzer_status,
         'code'     : 200,
         'type'     : 'buzzerSensorCloseSuccess',
         'msg'      : '蜂鳴器已經開啟！'
      }), 200
   else:
      return jsonify({
         'pin'        : pin_num,
         'mode'       : pin_mode,
         'accessory'  : 'buzzer',
         'status'     : buzzer_status,
         'error_code' : 400,
         'error_type' : 'buzzerSensorReopen',
         'error_msg'  : '請勿重複開啟蜂鳴器！'
      }), 400

@buzzer_blueprint.route("/off")
def off_led():
   global buzzer_status
   global pin_num
   global pin_mode
   # 判斷蜂鳴器是否已經打開
   if buzzer_status:
      # TODO: 檢查元件已經正確被關閉
      buzzer_status = False
      data = {
         'pin'      : pin_num,
         'mode'     : pin_mode,
         'code'     : 200,
         'accessory': 'buzzer',
         'status'   : buzzer_status,
         'type'     : 'buzzerSensorCloseSuccess',
         'msg'      : '蜂鳴器已經關閉！'
      }
      socketio.emit('Buzzer_off_publish_server', data, json=True, namespace='/pi', broadcast=True)
      return jsonify(data), 200
   else:
      return jsonify({
         'pin'       : pin_num,
         'mode'      : pin_mode,
         'accessory' : 'buzzer',
         'status'    : buzzer_status,
         'error_code': 400,
         'error_type': 'buzzerSensorUnopen',
         'error_msg' : '請勿在未開啟狀態關閉蜂鳴器！！'
      }), 400

   return jsonify(data), 400
