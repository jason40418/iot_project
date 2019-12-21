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
infrared_blueprint = Blueprint('infrared', __name__)
infrared_status = False
pin_num = config.getValue('infrared', 'pin')
pin_mode = config.getValue('infrared', 'mode')

def check_infrared_status():
    global infrared_status
    socketio.emit('infrared_status_check_pub_system', {'action': 'check'}, json=True, broadcast=True, namespace='/pi')
    time.sleep(.5)

@socketio.on('infrared_status_pub_pi', namespace='/pi')
def bread_infrared_status(data):
    global infrared_status
    infrared_status = data['status']
    # 將目前狀態發布給Client端（結束也會主動發布給Server）
    emit_data = get_accessory_publish_data('infrared_sensor', infrared_status)
    socketio.emit('accessory_status_pub_client', emit_data, json=True, broadcast=True, namespace='/client')

@infrared_blueprint.route("/on")
def main():
   global infrared_status
   global pin_num
   global pin_mode

   # 判斷紅外線感測器是否已經打開
   if not infrared_status:
      proc = subprocess.Popen(["python3 FaceIdentify.py"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)
      # TODO: 檢查元件已經正確被開啟
      infrared_status = True
      return jsonify({
         'pin'      : pin_num,
         'mode'     : pin_mode,
         'accessory': 'infrared_sensor',
         'status'   : infrared_status,
         'code'     : 200,
         'type'     : 'InfraredSensorCloseSuccess',
         'msg'      : '紅外線感測器已經開啟！'
      }), 200
   else:
      return jsonify({
         'pin'        : pin_num,
         'mode'       : pin_mode,
         'accessory'  : 'breath_light',
         'status'     : infrared_status,
         'error_code' : 400,
         'error_type' : 'InfraredSensorReopen',
         'error_msg'  : '請勿重複開啟紅外線感測器！'
      }), 400

@infrared_blueprint.route("/off")
def off_led():
   global infrared_status
   global pin_num
   global pin_mode
   # 判斷紅外線感測器是否已經打開
   if infrared_status:
      # TODO: 檢查元件已經正確被關閉
      infrared_status = False
      data = {
         'pin'      : pin_num,
         'mode'     : pin_mode,
         'code'     : 200,
         'accessory': 'infrared_sensor',
         'status'   : infrared_status,
         'type'     : 'InfraredSensorCloseSuccess',
         'msg'      : '紅外線感測器已經關閉！'
      }
      socketio.emit('infrared_off_publish_server', data, json=True, namespace='/pi', broadcast=True)
      return jsonify(data), 200
   else:
      return jsonify({
         'pin'       : pin_num,
         'mode'      : pin_mode,
         'accessory' : 'infrared_sensor',
         'status'    : infrared_status,
         'error_code': 400,
         'error_type': 'InfraredSensorUnopen',
         'error_msg' : '請勿在未開啟狀態關閉紅外線感測器！！'
      }), 400

   return jsonify(data), 400
