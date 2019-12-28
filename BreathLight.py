import RPi.GPIO as gpio
import time
import socketio
from model.util.Config import Config
from model.util.Socket import Socket
from model.util.AQI import AQI

# 取得設定檔案
config = Config()
led_pin_num = int(config.getValue('led', 'pin'))
led_pin_mode = config.getValue('led', 'mode')

# 初始化呼吸燈速度
aqi = AQI()
METRIX = ['PM1.0', 'PM2.5', 'PM10.0', '0.3um+', '0.5um+', '1.0um+', '2.5um+', '5.0um+', '10.0um+']
score, total = aqi.get_latest_value(METRIX)
frequence = 100 - round(90 * (score/total), 0)

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
    pwm = gpio.PWM(led_pin_num, frequence)
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

    # 取得最新感測資料
    @sio.on('sensor_data_pub_system', namespace='/system')
    def latest(payload):
        global aqi
        global METRIX
        global frequence
        score, total = aqi.calc(METRIX, payload['data'])
        frequence = 100 - round(90 * (score/total), 0)
        print("[@BreahthLight] 目前分數（越低越佳）", score, "/", total)

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
        pwm.ChangeFrequency(frequence)
        print("[@BreahthLight] 目前頻率：", frequence)

        if not status:  break

    try:
        sio.call(event='LED_status_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
        print('wait')
    except socketio.exceptions.TimeoutError as err:
        print('timeout')
else:
    print("[@BreahthLight] 無法建立WebSocket連線，資料無法發送")

pwm.stop()
socket.close()
