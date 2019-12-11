from flask import Blueprint, jsonify
from flask import request, make_response, render_template
from model.util.General import public_key_require_page, token_no_require_page

from __main__ import app

# 定義
member_blueprint = Blueprint('member', __name__)

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
