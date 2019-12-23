import os, time
from flask import Flask, make_response, render_template, jsonify, send_from_directory, request, render_template_string, redirect
from flask_misaka import Misaka, markdown
from flask_socketio import SocketIO, send, emit
from model import Auth
from model.helper.SensorHelper import SensorHelper
from model.util import Config as cfg
from model.util import General
from model.util.General import token_no_require_page, get_current_datetime
import RPi.GPIO as GPIO

app = Flask(__name__)
# 讓JSON能直接顯示中文
app.config['JSON_AS_ASCII'] = False
Misaka(app, fenced_code=True, highlight=True, quote=True, math=True,
math_explicit=True, space_headers=True, hard_wrap=True, wrap=True,
footnotes=True, autolink=True)

root_dir = app.root_path
config = cfg.Config(root_dir)

socketio = SocketIO(app)
from controllers import AccessoryController, APIController, LEDController, WebSocketController, AvatarController, MemberController, DataController
from controllers import FaceController, InfraredController

SENSOR_DATA_LIST = SensorHelper.SENSOR_LIST

#####################################
# 註冊，包含前輟字
#####################################
app.register_blueprint(APIController.api_blueprint, url_prefix='/api')
app.register_blueprint(LEDController.led_blueprint, url_prefix='/api/led')
app.register_blueprint(InfraredController.infrared_blueprint, url_prefix='/api/infrared')
app.register_blueprint(AvatarController.avatar_blueprint, url_prefix='/member/avatar')
app.register_blueprint(MemberController.member_blueprint, url_prefix='/member')
app.register_blueprint(FaceController.face_blueprint, url_prefix='/face')
app.register_blueprint(DataController.data_blueprint, url_prefix='/data')
app.register_blueprint(AccessoryController.accessory_blueprint, url_prefix='/accessory')

######################################
# Route
######################################
@app.route('/', methods=['GET'])
def index():
    result, data = SensorHelper.get_latest_data()
    resp = make_response(render_template('app/index.html', SENSOR_DATA = SENSOR_DATA_LIST, data=data))
    return resp

@app.route("/terms", methods=['GET'])
def term():
    resp = make_response(render_template('terms/latest.md'))
    return resp

######################################
# 靜態文件
######################################
# 處理要求favicon
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'favicon'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 處理靜態（static）文件路徑
@app.route('/<path:path>', methods=['GET'])
def static_file(path):
    static_path = os.path.join(root_dir, 'static', path)
    print(static_path)
    return app.send_static_file(static_path)

######################################
# 正確關閉伺服器
######################################
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    try:
        # 離開時清除掉GPIO所有設定
        GPIO.cleanup()
    except RuntimeWarning:
        print("[@App] 可能沒有任何channel被設定，沒有任何東西被清理！")

@app.route('/shutdown', methods=['GET'])
def shutdown():
    socketio.emit('server_clean_pub', data, json=True, broadcast=True, namespace='/pi')
    time.sleep(10)
    shutdown_server()
    return 'Server shutting down...'

# 除錯=True可讓更新後即時顯示，不用重開
if __name__ == '__main__':
    ip = config.getIPAddress()
    port = config.getValue('host', 'port')
    # 印出所有網頁路徑
    print(app.url_map)
    data = {
        'action': "清除可能未正確關閉的元件！"
    }
    socketio.emit('server_clean_pub', data, json=True, broadcast=True, namespace='/pi')
    GPIO.cleanup()
    socketio.run(app, host= '0.0.0.0', port=port, debug=True)
