from flask import Blueprint, jsonify, request, make_response
from datetime import datetime
from model.entity.Member import Member
from model.util.General import private_key_require_page, convert_byte_to_dict, generate_token
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
        data.update({
            'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key_id'     : reqest_data['id']
        })
        return jsonify(data), data['error_code']
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

@api_blueprint.route('/member/login', methods=['POST'])
@private_key_require_page('login')
def member_login(decode_result, data):
    # 取回Request資料
    reqest_data = request.json

    # 如果私鑰解密過程失敗
    if not decode_result:
        data.update({
            'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key_id'     : reqest_data['id']
        })
        return jsonify(data), data['error_code']
    else:
        # TODO: 使用者傳入資料後端需要再做驗證（含檢查所有key存在和資料格式）
        status, result, code = MemberHelper.verify(data['account'], data['password'])
        # 增加其他要回傳的欄位資料
        result.update({'datetime' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'key_id': reqest_data['id']})
        # 如果帳號密碼檢查成功（核發token並設為cookies）
        if status:
            get_member_result, member_result, status = MemberHelper.get(data['account'])

            # 取回原本會員資料結果成功
            if get_member_result:
                # 取得會員帳號和暱稱
                account = member_result.get_all_parameter()['account']
                name = member_result.get_all_parameter()['name']
                result.update({'account': account, 'name': name})
                resp = make_response(jsonify(result), status)
                # 產生token
                token, expired_time = generate_token(result ,'login_expire')
                # 設定 cookies
                resp.set_cookie(key='token', value=token, expires=expired_time)
                print(result)
            # 取回會員資料失敗
            else:
                resp = make_response(jsonify(member_result), status)
                # 設定token過期
                resp.set_cookie(key='token', value='', expires=0)
        # 回傳錯誤訊息
        else:
            resp = make_response(jsonify(result), code)
            # 設定token過期
            resp.set_cookie(key='token', value='', expires=0)
        return resp
