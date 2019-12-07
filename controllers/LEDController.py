'''
呼吸燈不能用接收是否有輸出的狀態GPIO.input({{pin_number}})來判斷是否有開啟，因為暗燈時會呈現為0
'''
import subprocess
import RPi.GPIO as GPIO
from flask import Blueprint, jsonify, render_template, request
from __main__ import app, socketio
from model.util import Config as cfg
from flask_socketio import send, emit

# 取得設定檔案
root_dir = app.root_path
config = cfg.Config(root_dir)

# 定義
led_blueprint = Blueprint('led', __name__)
led_status = False
led_pin_num = config.getValue('led', 'pin')
led_pin_mode = config.getValue('led', 'mode')

@socketio.on('bread_led_status')
def bread_led_status(data):
   global led_status
   led_status = data['status']
   print(data)

@led_blueprint.route("/")
def main():
   global led_status
   global led_pin_num
   global led_pin_mode

   # 判斷呼吸燈是否已經打開
   if not led_status:
      proc = subprocess.Popen(["python3 model/BreathLight.py"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)
      led_status = True
      return jsonify({
         'pin'     : led_pin_num,
         'mode'    : led_pin_mode,
         'status'  : str(led_status),
         'message' : '呼吸燈已經開啟！'
      }), 302
   else:
      return jsonify({
         'pin'     : led_pin_num,
         'mode'    : led_pin_mode,
         'status'  : str(led_status),
         'message' : '請勿重複開啟呼吸燈！'
      }), 400

@led_blueprint.route("/off")
def off_led():
   global led_status
   global led_pin_num
   global led_pin_mode
   # 判斷呼吸燈是否已經打開
   if led_status:
      data = {
         'pin'     : led_pin_num,
         'mode'    : led_pin_mode,
         'status'  : str(led_status),
         'message' : '呼吸燈已經關閉！'
      }
      socketio.emit('server_led_off', data, json=True, broadcast=True)
      led_status = False
      return jsonify(data), 302
   else:
      return jsonify({
         'pin'     : led_pin_num,
         'mode'    : led_pin_mode,
         'status'  : str(led_status),
         'message' : '請勿在未開啟狀態關閉呼吸燈！'
      }), 400
   
   return jsonify(data), 302