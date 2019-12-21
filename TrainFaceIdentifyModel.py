'''
訓練模型
'''
import subprocess, time
import socketio
from model.util.Config import Config
from model.util.Socket import Socket

# TODO: 檢查模型是否訓練成功或發生錯誤
# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()
config = Config()

param = {
    'dataset'           : config.getValue('face_model', 'dataset'),
    'embeddings'        : config.getValue('face_model', 'embeddings'),
    'detector'          : config.getValue('face_model', 'detector'),
    'embedding_model'   : config.getValue('face_model', 'embedding_model'),
    'recognizer'        : config.getValue('face_model', 'recognizer'),
    'le'                : config.getValue('face_model', 'le')
}

# 如果WebSocker建立連線成功
if connection:
    status = True

    proc = subprocess.Popen(["bash train_model.sh -d '" + param['dataset'] + "' -b '" + param['embeddings'] + "'\
                -t '" + param['detector'] + "' -m '" + param['embedding_model'] + "'\
                -r '" + param['recognizer'] + "' -e '" + param['le'] + "'"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)

    proc.communicate()

    try:
        sio.call(event='model_train_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
    except socketio.exceptions.TimeoutError as err:
        print('timeout')
else:
    print("[@TrainFaceIdentifyModel] 無法建立WebSocket連線，資料無法發送")

socket.close()
