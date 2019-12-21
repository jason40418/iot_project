'''
訓練模型
'''
import subprocess, time
import socketio
from model.util.Socket import Socket

# TODO: 檢查模型是否訓練成功或發生錯誤
# 初始化 socket
socket = Socket()
connection = socket.connect()
sio = socket.get_socket()

# 如果WebSocker建立連線成功
if connection:
    status = True

    proc = subprocess.Popen(["bash train_model.sh -d 'dataset' -b 'output/embeddings.pickle'\
                -t 'face_detection_model' -m 'openface_nn4.small2.v1.t7'\
                -r 'output/recognizer.pickle' -e 'output/le.pickle'"], shell=True,
               stdin=None, stdout=None, stderr=None, close_fds=True)

    proc.communicate()

    try:
        sio.call(event='model_train_pub_pi', data={'status': False}, namespace='/pi', timeout=30)
    except socketio.exceptions.TimeoutError as err:
        print('timeout')
else:
    print("[@TrainFaceIdentifyModel] 無法建立WebSocket連線，資料無法發送")

socket.close()
