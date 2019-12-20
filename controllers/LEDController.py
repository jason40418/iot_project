'''
呼吸燈不能用接收是否有輸出的狀態GPIO.input({{pin_number}})來判斷是否有開啟，因為暗燈時會呈現為0
'''
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
led_blueprint = Blueprint('led', __name__)
led_status = False
led_pin_num = config.getValue('led', 'pin')
led_pin_mode = config.getValue('led', 'mode')

def check_led_status():
    global led_status
    socketio.emit('LED_status_check_pub_system', {'action': 'check'}, json=True, broadcast=True, namespace='/pi')
    time.sleep(.5)

@socketio.on('LED_status_pub_pi', namespace='/pi')
def bread_led_status(data):
    global led_status
    led_status = data['status']
    # 將目前狀態發布給Client端（結束LED也會主動發布給Server）
    emit_data = get_accessory_publish_data('breath_light', led_status)
    socketio.emit('accessory_status_pub_client', emit_data, json=True, broadcast=True, namespace='/client')

@led_blueprint.route("/on")
def main():
   global led_status
   global led_pin_num
   global led_pin_mode

   # 判斷呼吸燈是否已經打開
   if not led_status:
      proc = subprocess.Popen(["python3 BreathLight.py"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)
      # TODO: 檢查LED已經正確被開啟
      led_status = True
      return jsonify({
         'pin'      : led_pin_num,
         'mode'     : led_pin_mode,
         'accessory': 'breath_light',
         'status'   : led_status,
         'code'     : 200,
         'type'     : 'BreathLightCloseSuccess',
         'msg'      : '呼吸燈已經開啟！'
      }), 200
   else:
      return jsonify({
         'pin'        : led_pin_num,
         'mode'       : led_pin_mode,
         'accessory'  : 'breath_light',
         'status'     : led_status,
         'error_code' : 400,
         'error_type' : 'BreathLightReopen',
         'error_msg'  : '請勿重複開啟呼吸燈！'
      }), 400

@led_blueprint.route("/off")
def off_led():
   global led_status
   global led_pin_num
   global led_pin_mode
   # 判斷呼吸燈是否已經打開
   if led_status:
      # TODO: 檢查LED已經正確被關閉
      led_status = False
      data = {
         'pin'      : led_pin_num,
         'mode'     : led_pin_mode,
         'code'     : 200,
         'accessory': 'breath_light',
         'status'   : led_status,
         'type'     : 'BreathLightCloseSuccess',
         'msg'      : '呼吸燈已經關閉！'
      }
      socketio.emit('LED_off_publish_server', data, json=True, namespace='/pi', broadcast=True)
      return jsonify(data), 200
   else:
      return jsonify({
         'pin'       : led_pin_num,
         'mode'      : led_pin_mode,
         'accessory' : 'breath_light',
         'status'    : led_status,
         'error_code': 400,
         'error_type': 'BreathLightUnopen',
         'error_msg' : '請勿在未開啟狀態關閉呼吸燈！！'
      }), 400

   return jsonify(data), 400
