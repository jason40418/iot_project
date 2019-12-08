from flask import Blueprint, jsonify, request
from datetime import datetime
from model.entity.Member import Member
from model.util.General import private_key_require_page, convert_byte_to_dict
from model.helper.MemberHelper import MemberHelper

# 定義
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/', methods=['GET'])
def api_index():
    return jsonify({'message': 'API路徑請求'}), 200

@api_blueprint.route('/member/duplicate_confirm', methods=['GET'])
def member_duplocate_confirm():
    # TODO: 使用者傳入資料後端需要再做驗證（含檢查所有key存在和資料格式）
    account = request.args.get('account')
    status, result, status_code = MemberHelper.check_duplicate_by_account(account)

    return jsonify(result), status_code

@api_blueprint.route('/member/register', methods=['POST'])
@private_key_require_page('register')
def member_register(decode_result, data):
    # 取回Request資料
    reqest_data = request.json

    # 如果私鑰解密過程失敗
    if not decode_result:
        return jsonify({
            'error_msg'  : data['error_msg'],
            'error_type' : data['error_type'],
            'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key_id'     : reqest_data['id']
        }), data['error_code']
    else:
        # TODO: 使用者傳入資料後端需要再做驗證（含檢查所有key存在和資料格式）
        # 檢查使用者名稱重複性
        duplicate_check, result, status_code = MemberHelper.check_duplicate_by_account(data['account'])
        if not duplicate_check:
            return jsonify(result), status_code

        m = Member(str(data['account']), str(data['name']), str(data['email']), str(data['password']), 'member')
        status, result, code = MemberHelper.create(m)
        # 增加其他要回傳的欄位資料
        result.update({'datetime' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'key_id': reqest_data['id']})
        return jsonify(result), code
