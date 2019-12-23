
from flask import Blueprint, jsonify
from flask import request, make_response, render_template, abort
from model.util.General import public_key_require_page, token_no_require_page, token_require_page, get_datetime_label

from __main__ import app

# 定義
face_blueprint = Blueprint('face', __name__)

@face_blueprint.route("/", methods=['GET'])
def index():
    resp = make_response(render_template('app/face/latest.html'), 200)
    return resp

@face_blueprint.route("/insider", methods=['GET'])
def insider():
    resp = make_response(render_template('app/face/insider.html'), 200)
    return resp

@face_blueprint.route("/current", methods=['GET'])
def status():
    api_path = '/api/face/current'
    info = {
        'title'             : '即時目前環境人員',
        'url'               : api_path,
        'method'            : 'GET',
        'frequence'         : '即時（realtime）',
        'description'       : '顯示目前環境中所有人員',
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
                'col'       : "row",
                'zh_name'   : "人員數量"
            },
            {
                'col'       : "datetime",
                'zh_name'   : "資料獲取時間"
            },
            {
                'col'       : "data",
                'zh_name'   : "獲取的資料（可能無人，為空）"
            },
            {
                'col'       : "data > account",
                'zh_name'   : "人員帳戶名稱"
            },
            {
                'col'       : "data > datetime",
                'zh_name'   : "進入環境時間"
            },
            {
                'col'       : "data > id",
                'zh_name'   : "進入編號"
            }
        ]
    }
    resp = make_response(render_template('/app/open_data.html', api_path=api_path, info=info), 200)
    return resp
