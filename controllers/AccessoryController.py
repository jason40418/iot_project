import datetime, json
import pandas as pd
from flask import Blueprint, jsonify
from flask import request, make_response, render_template, abort
from controllers import LEDController, AvatarController, InfraredController, BuzzerController, MotorController
from model.util.General import public_key_require_page, token_no_require_page, token_require_page, get_datetime_label, get_current_datetime

from __main__ import app

# 定義
accessory_blueprint = Blueprint('accessory', __name__)

def get_curr_accessory_status():
    LEDController.check_led_status()
    BuzzerController.check_buzzer_status()
    InfraredController.check_infrared_status()
    MotorController.check_motor_status()
    data = {
        'msg': '取得所有可控制元件成功！',
        'type' : 'FetchAccessoryStatusSuccess',
        'status' : 200,
        'datetime' : get_current_datetime("%Y-%m-%d %H:%M:%S"),
        'model_train' : AvatarController.avatar_model_during_train,
        'infrared_sensor' : InfraredController.infrared_status,
        'buzzer' : BuzzerController.buzzer_status,
        'motor' : MotorController.motor_status,
        'breath_light' : LEDController.led_status
    }
    return data

@accessory_blueprint.route("/", methods=['GET'])
def index():
    data = json.dumps(get_curr_accessory_status(), ensure_ascii=False, indent = 4, sort_keys=True)
    resp = make_response(render_template('/app/accessory/index.html', data=data), 200)
    return resp

@accessory_blueprint.route("/status", methods=['GET'])
def status():
    api_path = '/api/accessory/status'
    info = {
        'title'             : '元件狀態',
        'url'               : api_path,
        'method'            : 'GET',
        'frequence'         : '即時（realtime）',
        'description'       : '用於獲取目前所有元件之運作狀態',
        'col': [
            {
                'col'       : "type",
                'zh_name'   : "資料獲取訊息狀態"
            },
            {
                'col'       : "msg",
                'zh_name'   : "資料獲取訊息狀態（中文）"
            },
            {
                'col'       : "status",
                'zh_name'   : "資料獲取之HTTP狀態碼"
            },
            {
                'col'       : "datetime",
                'zh_name'   : "資料獲取時間"
            },
            {
                'col'       : "model_train",
                'zh_name'   : "資料獲取時間"
            },
            {
                'col'       : "breath_light",
                'zh_name'   : "呼吸燈狀態"
            }
        ]
    }
    resp = make_response(render_template('/app/open_data.html', api_path=api_path, info=info), 200)
    return resp
