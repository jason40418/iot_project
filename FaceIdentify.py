import RPi.GPIO as gpio
import time
import socketio
from model.util.Config import Config
from model.util.Socket import Socket

gpio.setwarnings(False)

# 取得設定檔案
config = Config()

pin_mode = config.getValue('infrared', 'mode')
pin_num = int(config.getValue('infrared', 'pin'))
led_pin_num = int(config.getValue('infrared', 'led_pin'))

gpio.setmode(gpio.BCM)

# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()

# 如果WebSocker建立連線成功
if connection:
    #Read output from PIR motion sensor
    gpio.setup(pin_num, gpio.IN)
    # LED output pin
    gpio.setup(led_pin_num, gpio.OUT)

    @sio.on('infrared_off_publish_server', namespace='/pi')
    @sio.on('server_clean_pub', namespace='/pi')
    def on_message(data):
        global status
        status = False

    @sio.on('infrared_status_check_pub_system', namespace='/pi')
    def check(data):
        print('[@FaceIdentify] Infrared Check...')
        sio.emit('infrared_status_pub_pi', {'status': True, 'method': '被動'}, namespace='/pi')

    status = True

    while True:
        # 讓LED 發送
        sio.emit('infrared_status_pub_pi', {'status': True}, namespace='/pi')
        i = gpio.input(pin_num)
        if i == 0:
            print("No intruders", i)
            gpio.output(led_pin_num, 0)  #Turn OFF LED
            time.sleep(0.1)
        elif i == 1:
            print("Intruder detected", i)
            gpio.output(led_pin_num, 1)  #Turn ON LED
            time.sleep(0.1)

        if not status:  break
        time.sleep(1)
        if not status:  break

    gpio.output(led_pin_num, 0)  #Turn OFF LED

    try:
        sio.call(event='infrared_status_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
    except socketio.exceptions.TimeoutError as err:
        print('timeout')
else:
    print("[@FaceIdentify] 無法建立WebSocket連線，資料無法發送")

socket.close()
