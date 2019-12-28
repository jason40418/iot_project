import RPi.GPIO as GPIO
import time
import socketio
from model.util.Config import Config
from model.util.Socket import Socket
from model.util.AQI import AQI
import random

def beep(seconds):
    GPIO.output(PIN_NUM, True)
    time.sleep(seconds)
    GPIO.output(PIN_NUM, False)

def beep_action(sec, sleep_sec):
    beep(sec)
    time.sleep(sleep_sec)

# 取得設定檔案
config = Config()
PIN_NUM = int(config.getValue('buzzer', 'pin'))
PIN_MODE = config.getValue('buzzer', 'mode')

# 初始化蜂鳴器速度
aqi = AQI()
METRIX = ['CO', 'LPG', 'Smoke']
score, total = aqi.get_latest_value(METRIX)
SLEEP = 1 * ((total-score)/total)

# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()

# 如果WebSocker建立連線成功
if connection:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_NUM, GPIO.OUT)

    @sio.on('buzzer_off_publish_server', namespace='/pi')
    @sio.on('server_clean_pub', namespace='/pi')
    def on_message(data):
        print("[@Buzzer]TEST")
        global status
        status = False

    @sio.on('buzzer_status_check_pub_system', namespace='/pi')
    def check(data):
        print('[@Buzzer] Buzzer Check...')
        sio.emit('buzzer_status_pub_pi', {'status': True, 'method': '被動'}, namespace='/pi')

    # 取得最新感測資料
    @sio.on('sensor_data_pub_system', namespace='/system')
    def latest(payload):
        global aqi
        global METRIX
        global SLEEP
        score, total = aqi.calc(METRIX, payload['data'])
        SLEEP = 1 * ((total-score)/total)
        print("[@Buzzer] 目前分數（越低越佳）", score, "/", total)

    status = True

    # Change duty cycle for varying the brightness of buzzer.
    while status:
        sio.emit('buzzer_status_pub_pi', {'status': True}, namespace='/pi')
        beep_action(0.01, SLEEP)

    try:
        sio.call(event='buzzer_status_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
        print('wait')
    except socketio.exceptions.TimeoutError as err:
        print('timeout')
else:
    print("[@Buzzer] 無法建立WebSocket連線，資料無法發送")

socket.close()
