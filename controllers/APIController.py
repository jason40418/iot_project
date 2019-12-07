from flask import Blueprint, jsonify, request
from datetime import datetime
from model.util.General import private_key_require_page, convert_byte_to_dict

# 定義
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/', methods=['GET'])
def api_index():
    return jsonify({'message': 'API路徑請求'}), 200

@api_blueprint.route('/member/duplicate_confirm', methods=['GET'])
def member_duplocate_confirm():
    account = request.args.get('account')
    return jsonify({
        'msg'     : "此帳號為新使用者，可以使用",
        'type'    : "AccountPassVerify",
        'account' : account
        }), 200

    return jsonify({
        'error_msg'  : "此帳號資料庫已經存在，請勿重複註冊",
        'error_type' : "AccountDuplicateError",
        'account'    : account
        }), 400

@api_blueprint.route('/member/register', methods=['POST'])
@private_key_require_page('register')
def member_register(result, data):
    # 取回Request資料
    reqest_data = request.json

    # 如果私鑰解密過程失敗
    if not result:
        return jsonify({
            'error_msg'  : data['error_msg'],
            'error_type' : data['error_type'],
            'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key_id'     : reqest_data['id']
        }), data['error_code']
    else:
        # TODO: 使用者傳入資料後端需要再做驗證（含檢查帳戶重複性與資料格式）
        print(data)

        return jsonify({
            #'msg'  : "此帳號為新使用者，可以使用",
            #'type' : "AccountPassVerify",
            'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key_id'     : reqest_data['id']
        }), 200


