import datetime
import pandas as pd
from flask import Blueprint, jsonify
from flask import request, make_response, render_template, abort
from controllers import LEDController
from model.util.General import public_key_require_page, token_no_require_page, token_require_page, get_datetime_label, get_current_datetime

from __main__ import app

# 定義
accessory_blueprint = Blueprint('accessory', __name__)

@accessory_blueprint.route("/", methods=['GET'])
def index():
    resp = make_response(render_template('/app/accessory/index.html'), 200)
    return resp


@accessory_blueprint.route('/status', methods=['GET'])
def status():
    LEDController.check_led_status()
    data = {
        'msg': '取得所有可控制元件成功！',
        'type' : 'FetchAccessoryStatusSuccess',
        'status' : 200,
        'datetime' : get_current_datetime("%Y-%m-%d %H:%M:%S"),
        'breath_light' : LEDController.led_status
    }
    return jsonify(data), 200
