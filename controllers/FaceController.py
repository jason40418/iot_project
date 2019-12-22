
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
