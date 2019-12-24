import json, glob, os
from flask import Blueprint, jsonify, request, make_response
from datetime import datetime
from controllers import AccessoryController
from model.entity.Member import Member
from model.util.General import private_key_require_page, convert_byte_to_dict, generate_token, token_require_page
from model.helper.AccessHelper import AccessHelper
from model.helper.SensorHelper import SensorHelper
from model.helper.MemberHelper import MemberHelper
from model.helper.MemberPreferenceHelper import MemberPreferenceHelper

# 定義
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/', methods=['GET'])
def api_index():
    return jsonify({'message': 'API路徑請求'}), 200

@api_blueprint.route('/sensor/realtime', methods=['GET'])
def sensor_data():

    result, data = SensorHelper.get_latest_data()
    data.update({
        'type'  : 'SensorLastestDataFetchSuccess',
        'msg'   : '感應器最新資料取得成功',
        'code'  : 200
    })

    return jsonify(data), 200

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
        # 新增預設設定檔案資料
        MemberPreferenceHelper.add_default_value(str(data['account']))
        # 增加其他要回傳的欄位資料
        result.update({'datetime' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'key_id': reqest_data['id']})
        return jsonify(result), code

@api_blueprint.route('/member/edit', methods=['POST'])
@private_key_require_page('member_edit')
@token_require_page('/member/login')
def member_edit(payload, decode_result, data):
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

        # 取回會員資料
        status, result, code = MemberHelper.get(payload['account'])
        # 會員資料取回成功
        if status:
            m = result
            m.update(data['name'], data['email'], data['password'])
            status, result, code = MemberHelper.update(m)

        # 會員資料取回失敗
        else:
            pass

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

                # 取回預設偏好設定檔案
                pref, item_list = MemberPreferenceHelper.get_by_account(account)

                # 設定 cookies
                resp.set_cookie(key='token', value=token, expires=expired_time)
                resp.set_cookie(key='pref', value=str(json.dumps(pref, ensure_ascii=False)), expires=expired_time)
                print(result)
            # 取回會員資料失敗
            else:
                resp = make_response(jsonify(member_result), status)
                # 設定token過期
                resp.set_cookie(key='token', value='', expires=0)
                resp.set_cookie(key='pref', value='', expires=0)
        # 回傳錯誤訊息
        else:
            resp = make_response(jsonify(result), code)
            # 設定token過期
            resp.set_cookie(key='token', value='', expires=0)
            resp.set_cookie(key='pref', value='', expires=0)
        return resp

# 取得所有accessory的API
@api_blueprint.route('/accessory/status', methods=['GET'])
def accessory_status():
    data = AccessoryController.get_curr_accessory_status()
    return jsonify(data), 200

# 取得所有accessory的API
@api_blueprint.route('/avatar/status', methods=['GET'])
def avatar_status():
    data = dict()
    with open('static/json/face_folder.json') as json_file:
        data = json.load(json_file)
    return jsonify(data), 200

# 取得最新人臉辨識照片
@api_blueprint.route('/face/latest', methods=['GET'])
def latest_face():
    # TODO: 應該檢查取回的檔案是否都是圖片檔案
    list_of_files = glob.glob('static/images/identify/*')
    if len(list_of_files) != 0:
        latest_file = max(list_of_files, key=os.path.getctime)
        filename = latest_file.split('/')[-1]
        date = filename[0:4] + '-' + filename[4:6] + '-' + filename[6:8]
        time = filename[8:10] + ':' + filename[10:12] + ':' + filename[12:14]
        result =  {
            'datetime'  : date + ' ' + time,
            'filename'  : filename,
            'path'      : '/' + latest_file,
            'status'    : True
        }
    else:
        result =  {
            'datetime'  : '',
            'filename'  : '',
            'path'      : '',
            'status'    : False
        }

    return jsonify(result), 200

@api_blueprint.route('/member/access_record', methods=['GET'])
@token_require_page("/member/login")
def access_record(payload):
    account = payload['account']
    # 取回該名會員的進出記錄
    status, row, access_record = AccessHelper.get_records_by_name(account)
    return jsonify({
        'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status' : True,
        'msg'  : '會員進出紀錄取得成功',
        'type' : 'MemberAccessRecordFetchSuccess',
        'code' : 200,
        'data': access_record
    }), 200

@api_blueprint.route('/face/current', methods=['GET'])
def curr_face_in_room():
    status, row, data = AccessHelper.get_all()
    return jsonify({
        'datetime'   : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status' : True,
        'msg'  : '環境目前人員',
        'type' : 'CurrentFaceInRoomFetchSuccess',
        'code' : 200,
        'row'  : row,
        'data' : data
    }), 200
