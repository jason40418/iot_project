import pandas as pd
from flask import Blueprint, jsonify
from flask import request, make_response, render_template, redirect
from model.helper.MemberHelper import MemberHelper
from model.util.General import public_key_require_page, token_no_require_page, token_require_page
from model.helper.SensorHelper import SensorHelper
from model.helper.MemberPreferenceHelper import MemberPreferenceHelper

from __main__ import app

# 定義
member_blueprint = Blueprint('member', __name__)

def get_perf_data(account):
    # 取回預設偏好設定檔案
    pref, item_list = MemberPreferenceHelper.get_by_account(account)
    # TODO: 檢查偏好設定是否有遺漏項目（edit也需要）
    item_df = pd.DataFrame(SensorHelper.SENSOR_LIST).set_index('id')
    return pref, item_df

@member_blueprint.route("/", methods=['GET'])
@token_require_page('/member/login', request_type='pages')
def index(payload):
    account = payload['account']
    # 取回會員資料
    status, result, code = MemberHelper.get(account)
    # 會員資料取回成功
    if status:
        # 取回偏好設定參數
        pref, item_df = get_perf_data(account)
        resp = make_response(render_template('app/member/index.html',
                        member=result.get_all_parameter(), pref=pref, item_df = item_df))
        return resp
    # 會員資料取回失敗，重新導向登入頁面
    else:
        resp = make_response(redirect(url, code=302))
        resp.set_cookie(key='token', value='', expires=0)
        return resp

@member_blueprint.route("/edit", methods=['GET'])
@token_require_page('/member/login', request_type='pages')
@public_key_require_page('member_edit', 'member_edit_rsa_key')
def edit(rsa, payload):
    account = payload['account']
    # 取回會員資料
    status, result, code = MemberHelper.get(account)
    # 會員資料取回成功
    if status:
        # 取回偏好設定參數
        pref, item_df = get_perf_data(account)
        resp = make_response(render_template('app/member/edit.html',
                        member=result.get_all_parameter(), rsa=rsa,
                        pref=pref, item_df = item_df))
        return resp
    # 會員資料取回失敗，重新導向登入頁面
    else:
        resp = make_response(redirect(url, code=302))
        resp.set_cookie(key='token', value='', expires=0)
        return resp

@member_blueprint.route("/register", methods=['GET'])
@token_no_require_page('/member')
@public_key_require_page('register', 'register_rsa_key')
def register(rsa):
    resp = make_response(render_template('app/member/register.html', rsa=rsa))
    return resp


@member_blueprint.route('/login', methods=['GET'])
@token_no_require_page('/member')
@public_key_require_page('login', 'login_rsa_key')
def login(rsa):
    resp = make_response(render_template('app/member/login.html', rsa=rsa))
    # 設定token過期
    resp.set_cookie(key='token', value='', expires=0)
    return resp

@member_blueprint.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/member/login'), 302)
    # 設定token過期
    resp.set_cookie(key='token', value='', expires=0)
    return resp
