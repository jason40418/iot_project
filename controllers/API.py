from flask import Blueprint, jsonify

# 定義
api = Blueprint('api', __name__)

@api.route("/", methods=['GET'])
def api_index():
    return jsonify({"message": "API路徑請求"}), 302