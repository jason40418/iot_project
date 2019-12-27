import socketio
from time import sleep
from model.accessory.DHT import DHT
from model.util.Config import Config
from model.util.Socket import Socket
from model.util.General import get_current_datetime, round_dict_value
from model.helper.SensorHelper import SensorHelper

# ==============================================================================
# 設定檔案、參數和SocketIO
# ==============================================================================
# 設定Config
config = Config()

# 儲存讀取失敗的裝置
fail_list = list()
# 儲存觀測的數值
sensor_data = dict()
# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()

# ==============================================================================
# 收到監測數據後，中斷連線
# ==============================================================================
'''
01. AM2302（DHT22）溫濕感應器
'''
dht_sensor = config.getValue('AM2302', 'sensor')
dht_pin = config.getValue('AM2302', 'pin')
dht = DHT(dht_sensor, dht_pin)
dht_result, dht_data = dht.get_data()
sensor_data.update(dht_data)
if not dht_result:  fail_list.append('AM2302')

'''
02. PMS5003
'''
from model.accessory.PMS import PMS
pms_sensor = PMS()
pms_result, pms_data = pms_sensor.get_data()
sensor_data.update(pms_data)
if not pms_result:  fail_list.append('PMS5003')

'''
03. MQ2 + MCP3008
'''
from model.accessory.MQ2 import MQ2
mq_sensor = MQ2()
mq_result, mq_data = mq_sensor.get_data()
sensor_data.update(mq_data)
if not mq_result:  fail_list.append('MQ2')

# ==============================================================================
# 將監測資料新增至資料庫
# ==============================================================================
record_id = SensorHelper.get_new_record_id()
SensorHelper.insert_sensor_data(sensor_data, record_id)
SensorHelper.update_fail_list(fail_list, record_id)

# ==============================================================================
# 透過WebSocket發送資料到伺服器端
# ==============================================================================
# 如果WebSocker建立連線成功
if connection:
    payload = {
        'id' : record_id,
        'datetime': get_current_datetime("%Y-%m-%d %H:%M:%S"),
        'fail' : fail_list,
        'data' : round_dict_value(sensor_data)
    }
    # 發送資料到伺服器端
    try:
        sio.call(event='sensor_data_pub_pi', data=payload, namespace='/pi', timeout=30)
    except socketio.exceptions.TimeoutError as err:
        print('timeout')

else:
    print("[@AutoMonitor] 無法建立WebSocket連線，資料無法發送")

socket.close()
