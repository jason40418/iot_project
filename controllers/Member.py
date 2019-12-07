from flask import Blueprint, jsonify
from flask import request, make_response, render_template
from model.util.General import public_key_require_page

from __main__ import app

# 定義
member_blueprint = Blueprint('member', __name__)

@member_blueprint.route("/register", methods=['GET'])
@public_key_require_page('register', 'register_rsa_key')
def register(rsa):
    resp = make_response(render_template('app/member/register.html', rsa=rsa))
    return resp
