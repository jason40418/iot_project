import RPi.GPIO as GPIO
import time
import math
import socketio
from model.util.Config import Config
from model.util.Socket import Socket
from model.util.AQI import AQI
import random

# 取得設定檔案
config = Config()
PIN_NUM = int(config.getValue('motor', 'pin'))
PIN_MODE = config.getValue('motor', 'mode')

# 初始化馬達角度
ANGLE = [2.5, 5, 7.5, 10, 12.5]
aqi = AQI()
METRIX = ['temperature', 'humidity']
score, total = aqi.get_latest_value(METRIX)
idx = math.floor(score / (math.ceil(total/5)))

# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()

# 如果WebSocker建立連線成功
if connection:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_NUM, GPIO.OUT)
    p = GPIO.PWM(PIN_NUM, 50)
    # Initialization
    p.start(ANGLE[idx])

    @sio.on('motor_off_publish_server', namespace='/pi')
    @sio.on('server_clean_pub', namespace='/pi')
    def on_message(data):
        global status
        status = False

    @sio.on('motor_status_check_pub_system', namespace='/pi')
    def check(data):
        print('[@Motor] Motor Check...')
        sio.emit('Motor_status_pub_pi', {'status': True, 'method': '被動'}, namespace='/pi')

    # 取得最新感測資料
    @sio.on('sensor_data_pub_system', namespace='/system')
    def latest(payload):
        global aqi
        global METRIX
        global idx
        score, total = aqi.calc(METRIX, payload['data'])
        idx = math.floor(score / (math.ceil(total/5)))
        print("[@Motor] 目前分數（越低越佳）", score, "/", total)

    status = True

    # Change duty cycle for varying the brightness of Motor.
    while status:
        sio.emit('motor_status_pub_pi', {'status': True}, namespace='/pi')
        print(ANGLE[idx])
        p.ChangeDutyCycle(ANGLE[idx])
        time.sleep(1)

    try:
        sio.call(event='motor_status_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
        print('wait')
    except socketio.exceptions.TimeoutError as err:
        print('timeout')

else:
    print("[@Motor] 無法建立WebSocket連線，資料無法發送")

p.start(2.5)
p.stop()
socket.close()
