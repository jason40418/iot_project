import RPi.GPIO as gpio
import time
import socketio
from model.util.Config import Config
from model.util.Socket import Socket

# 取得設定檔案
config = Config()
led_pin_num = int(config.getValue('led', 'pin'))
led_pin_mode = config.getValue('led', 'mode')

# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()

# 如果WebSocker建立連線成功
if connection:
    # Use BCM mode to numbering
    gpio.setmode (gpio.BCM)

    # Set pin number as an output
    gpio.setup(led_pin_num, gpio.OUT)

    # Set pin number as PWM output with 100Hz
    pwm = gpio.PWM(led_pin_num, 200)
    # Start up with 0% duty cycle
    pwm.start(0)

    @sio.on('LED_off_publish_server', namespace='/pi')
    @sio.on('server_clean_pub', namespace='/pi')
    def on_message(data):
        global status
        status = False

    @sio.on('LED_status_check_pub_system', namespace='/pi')
    def check(data):
        print('[@BreathLight] LED Check...')
        sio.emit('LED_status_pub_pi', {'status': True, 'method': '被動'}, namespace='/pi')

    status = True

    # Change duty cycle for varying the brightness of LED.
    while True:
        # 讓LED 發送
        sio.emit('LED_status_pub_pi', {'status': True}, namespace='/pi')
        # Execute duty cycle from 0% to 49%
        for x in range (50):
            if not status:  break
            pwm.ChangeDutyCycle(x)
            # Sleep for 100m second
            time.sleep(.1)

        # Execute duty cycle from 49% to 0%
        for x in range (50):
            if not status:  break
            pwm.ChangeDutyCycle(50-x)
            # Sleep for 100m second
            time.sleep(.1)

        time.sleep(.5)

        if not status:  break

    try:
        sio.call(event='LED_status_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
        print('wait')
    except socketio.exceptions.TimeoutError as err:
        print('timeout')
else:
    print("[@BreahthLight] 無法建立WebSocket連線，資料無法發送")

socket.close()
