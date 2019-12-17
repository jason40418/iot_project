import datetime
import pandas as pd
from flask import Blueprint, jsonify
from flask import request, make_response, render_template, abort
from model.helper.SensorHelper import SensorHelper
from model.util.General import public_key_require_page, token_no_require_page, token_require_page

from __main__ import app

# 定義
data_blueprint = Blueprint('data', __name__)

sensor = SensorHelper.SENSOR_LIST

def get_sensor_data(name):
    result = False
    data = dict()

    for item in sensor:
        if item['id'] == name:
            result = True
            data = item
            break

    return result, data

def his_df_to_list(df):
    return {
        'label' : df['datetime'].tolist() if 'datetime' in df else [],
        'high'  : df['high'].tolist() if 'high' in df else [],
        'low'   : df['low'].tolist() if 'low' in df else [],
        'mean'  : df['value'].tolist() if 'value' in df else []
    }


@data_blueprint.route("/history/<string:accessory>", methods=['GET'])
def index(accessory):
    day_para = request.args.get('day')
    try:
        day = int(day_para)
         # 處裡使用者輸入為負值的bug
        day = 30 if day < 0 else day
    except:
        day = 30

    item = accessory.lower()
    result, data = get_sensor_data(accessory)
    if result:
        # 取得該感測資料單位
        unit = data['unit']
        # 取得現在時間字串
        dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 取得感測歷史資料
        his_status, df, df_h, row, day_info = SensorHelper.get_sensor_his_data(accessory, day)
        # 將感測資料/小時感測資料轉換成list
        his_chart = his_df_to_list(df)
        his_chart_h = his_df_to_list(df_h)
        # 計算資料長度與數量
        his_chart_length = len(his_chart['label'])
        # 取得統計的平均數據
        statist_header, statist_data = SensorHelper.get_statist_data(accessory, [
            { 'minutes': 60}, { 'days': 1}, { 'days': 7}, { 'all': True},
        ], ['This Hour', 'Last Day', 'Last Week', 'All Time'])
        statist_icon = ['fa fa-heartbeat text-danger', 'fa fa-moon-o text-warning', 'fa fa-paper-plane-o text-primary', 'fa fa-history text-secondary']
        resp = make_response(
            render_template('/app/data_center/history.html',
                sensor=data, his_status=his_status, his_df=df, his_chart=his_chart,
                his_df_h=df_h, his_chart_h=his_chart_h, day_info=day_info, unit = unit,
                statist_header = statist_header, statist_data=statist_data, statist_icon=statist_icon,
                curr_date=dt_string, row=row, his_chart_length=his_chart_length), 200)
        return resp
    else:
        abort(404)
