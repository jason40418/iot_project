import RPi.GPIO as gpio
import time
import socketio
from util import Config as cfg

# 取得設定檔案
config = cfg.Config()
led_pin_num = int(config.getValue('led', 'pin'))
led_pin_mode = config.getValue('led', 'mode')
ws = config.getWebSocketUrl()

# Use BCM mode to numbering
gpio.setmode (gpio.BCM)

# Set pin number as an output
gpio.setup(led_pin_num, gpio.OUT)

# Set pin number as PWM output with 100Hz
pwm = gpio.PWM(led_pin_num, 200)
# Start up with 0% duty cycle
pwm.start(0)

sio = socketio.Client()
sio.connect(ws)

@sio.on('server_led_off')
@sio.on('server_clean')
def on_message(data):
    global status
    status = False
    sio.disconnect()

@sio.on('server_led_check')
def check(data):
    print('[@BreathLight] LED Check...')
    sio.emit('bread_led_status', {'status': True, 'method': '被動'})

status = True

# Change duty cycle for varying the brightness of LED.
while True:
    # 讓LED 發送
    sio.emit('bread_led_status', {'status': True})
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
    
    if not status:  break

sio.emit('bread_led_status', {'status': False})
    