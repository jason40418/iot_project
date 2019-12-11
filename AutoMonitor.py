import socketio
import Adafruit_DHT

from model.util.Config import Config

config = Config()
print(config.getValue('AM2302', 'sensor'))

# sio = socketio.Client()
# sio.connect('http://192.168.1.111:3000')

# @sio.on('server_receive')
# def on_message(data):
#     print(data)
#     sio.disconnect()

# sio.emit('front-end-publish', {'foo': 'bar'})

'''
溫濕感應器
'''

sensor_args = {
    '11'  : Adafruit_DHT.DHT11,
    '22'  : Adafruit_DHT.DHT22,
    '2302': Adafruit_DHT.AM2302
}
sensor = Adafruit_DHT.AM2302

pin = '21'
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
