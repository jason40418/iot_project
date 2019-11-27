import os
from flask import Flask, make_response, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, send, emit
from controllers.API import api
from model.util import Config as cfg

app = Flask(__name__)
root_dir = app.root_path
config = cfg.Config(root_dir)
#####################################
# 註冊，包含前輟字
#####################################
app.register_blueprint(api, url_prefix='/api')
socketio = SocketIO(app)

######################################
# Route
######################################
@app.route('/', methods=['GET'])
def index():
    resp = make_response(render_template('app/index.html'))
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

# debug=True 可讓更新後即時顯示，不用重開
if __name__ == '__main__':
    ip = config.getIPAddress()
    # 印出所有網頁路徑
    print(app.url_map)
    socketio.run(app, host= ip, port=3000, debug=True)
