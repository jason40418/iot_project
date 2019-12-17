import Adafruit_DHT
from model.util.Config import Config

class DHT():

    SENSOR_ARGS = {
        '11'  : Adafruit_DHT.DHT11,
        '22'  : Adafruit_DHT.DHT22,
        '2302': Adafruit_DHT.AM2302
    }

    def __init__(self, obj, pin):
        """[summary]

        Arguments:
            obj {[type]} -- [description]
            pin {[type]} -- [description]
        """
        self.__sensor = DHT.SENSOR_ARGS[obj] if obj != None else '2302'
        self.__pin = pin if pin != None else '21'

    def get_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.__sensor, self.__pin)
        # 讀取成功
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            # 判斷數值是否異常
            if humidity > 100 or humidity < 0:
                return False, {
                    'temperature' : None,
                    'humidity'    : None
                }
            else:
                return True, {
                    'temperature' : temperature,
                    'humidity'    : humidity
                }
        # 讀取失敗
        else:
            return False, {
                'temperature' : None,
                'humidity'    : None
            }
