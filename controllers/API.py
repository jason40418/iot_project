from flask import Blueprint, jsonify

# 定義
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/", methods=['GET'])
def api_index():
    return jsonify({"message": "API路徑請求"}), 302