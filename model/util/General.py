import ast, json, time, jwt, os
from datetime import datetime, timedelta, date
from functools import wraps
from flask import request, redirect, jsonify, make_response
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as ORI_RSA
from Crypto.Hash import SHA256
from base64 import b64decode
from time import localtime, strftime, sleep

from model.util.Key import Key
from model.util.Config import Config
from model.util.KeyRSA import KeyRSA
from model.entity.RSA import RSA
from model.helper.RSAHelper import RSAHelper

MIME_TYPE = {
    'gif' : "image/gif",
    'jpg' : "image/jpeg",
    'jpeg' : "image/jpeg",
    'png' : "image/png",
    'webp' : "image/webp",
    'svg' : "image/svg+xml",
    'xml' : "image/svg+xml",
    'tiff' : "image/tiff"
}

def get_folder_and_file_name(path):
    path_spilt_list = path.split('/')
    folder = "/"
    file_name = ""

    for i in range(len(path_spilt_list)):
        if i == (len(path_spilt_list) - 1):
            file_name = path_spilt_list[i]
        else:
            folder = folder + path_spilt_list[i] + "/"

    return folder, file_name

def token_no_require_page(url):
    '''
    若token存在，則不允許執行的頁面（需要檢查token有效性）
    正常來說過期的token應該會被瀏覽器自動清除
    '''
    # 需要增加產生RSA key
    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            resp = make_response(redirect(url, code=302))
            if 'token' in request.cookies:
                token = request.cookies.get('token')
                # 檢查解密成功性
                decode_status, payload = verify_token(token)
                if not decode_status:
                    return f(*args, **kwds)
                # 檢查token有效性
                elif time.time() > payload['expired_time']:
                    return f(*args, **kwds)
                else:
                    return resp
            else:
                return f(*args, **kwds)
        return wrapper
    return actual_decorator

def token_require_page(url, request_type='api'):
    '''需要token的頁面
    '''
    # 需要增加產生RSA key
    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            resp = make_response(redirect(url, code=302))
            if 'token' in request.cookies:
                token = request.cookies.get('token')
                # 檢查解密成功性
                decode_status, payload = verify_token(token)
                if not decode_status:
                    if request_type == 'api':
                        return jsonify({
                            'error_type': "TokenDecodeFail",
                            'error_msg': "使用者Token無法解析，請重新登入",
                            'error_code': 400
                        }), 400
                    else:
                        resp.set_cookie(key='token', value='', expires=0)
                        resp.set_cookie(key='pref', value='', expires=0)
                        return resp
                # 檢查token有效性
                elif time.time() > payload['expired_time']:
                    if request_type == 'api':
                        return jsonify({
                            'error_type': "TokenExpire",
                            'error_msg': "使用者Token已經失效，請重新登入",
                            'error_code': 401
                        }), 401
                    else:
                        resp.set_cookie(key='token', value='', expires=0)
                        resp.set_cookie(key='pref', value='', expires=0)
                        return resp
                else:
                    return f(payload, *args, **kwds)
            else:
                if request_type == 'api':
                    return jsonify({
                        'error_type': "TokenNotExist",
                        'error_msg': "請先登入再使用",
                        'error_code': 401
                    }), 401
                else:
                    resp.set_cookie(key='token', value='', expires=0)
                    resp.set_cookie(key='pref', value='', expires=0)
                    return resp
        return wrapper
    return actual_decorator

def public_key_require_page(usage, expire_para):
    # 需要增加產生RSA key
    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            # 取得RSA過期時間設定
            expire = Config().getValue('expire', expire_para)
            # 預設為10分鐘
            expire = 600 if expire == None else expire
            # 請求資源的IP位置
            request_ip = request.remote_addr
            rsa_key = KeyRSA()
            rsa = RSA(usage, request_ip, rsa_key, expire)

            data = {'id': rsa.get_rsa_key_id(), 'public_key': rsa_key.get_public_key()}

            return f(data, *args, **kwds)

        return wrapper
    return actual_decorator

def private_key_require_page(usage, key_id_key='id', encrypt_data_key='payload', check_keys=[]):
    # 需要使用PrivateKey的資料
    def actual_decorator(f):

        @wraps(f)
        def wrapper(*args, **kwds):
            # 請求資源的IP位置
            request_ip = request.remote_addr
            # 取回Request資料
            data = request.json
            # 檢查傳入的資料keys是否都存在
            keys_exist, not_found = check_data_keys_exist(data, check_keys)

            # payload資料
            key_id = data[key_id_key]
            # 檢查金鑰有效性（msg: 若金鑰有效則回傳為RSA Object，若無效則回傳dict）
            rsa_key_exist, row, decode_result = RSAHelper.check_key_vaild(key_id, request_ip, usage)

            # 預設解析結果為失敗（False）
            decode_status = False
            # 金鑰
            if rsa_key_exist:
                # 詳細金鑰
                rsa_key_info = decode_result.get_parameter()

                try:
                    # 設定私鑰
                    private_key = ORI_RSA.importKey(rsa_key_info['private_key'])
                    # 設定RSA私鑰與hash演算法組合
                    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
                    # 解密資料
                    decrypted_message = cipher.decrypt(b64decode(data[encrypt_data_key]))
                    # 將Byte轉換成JSON格式的dict
                    decode_status, decode_result = convert_byte_to_dict(decrypted_message)
                # 設定私鑰錯誤
                except (ValueError, TypeError):
                    decode_result = {
                        'error_type' : "PrivateKeyDecodeError",
                        'error_msg'  : "RSA私鑰設定錯誤",
                        'error_code' : 500
                    }
                # 產生解密密碼錯誤
                except AttributeError:
                    decode_result = {
                        'error_type' : "HashCombineError",
                        'error_msg'  : "RSA私鑰與Hash演算法組合錯誤",
                        'error_code' : 500
                    }
                # 資料解密錯誤
                finally:
                    # 回傳最終解析結果
                    if not decode_status:
                        decode_result = {
                            'error_type' : "KeyDecodeError",
                            'error_msg'  : "請求之內容無法進行解密",
                            'error_code' : 400
                        }
            else:
                # 金鑰失敗接續處理位置
                pass

            return f(decode_status, decode_result, *args, **kwds)

        return wrapper
    return actual_decorator

def convert_byte_to_dict(data):
    try:
        form = json.loads(data.decode('utf-8'))
    except:
        decode_result = {
            'error_type' : "JSONDecodeError",
            'error_msg'  : "JSON格式解析錯誤",
            'error_code' : 400
        }
        return False, decode_result
    return True, form

def check_data_keys_exist(data, keys=[]):
    not_found_keys = []
    for key in keys:
        if key not in data:
            not_found_keys.append(key)
    if len(not_found_keys) != 0:
        return False, not_found_keys
    else:
        return True, None

def generate_token(data, usage):
    '''
    核發token給使用者並使用伺服器預設定之固定私鑰加密
    '''
    expire_length = Config().getValue('token', usage)
    # 取得伺服器核發的私鑰（固定）
    private_key = Key().getPrivateKey()
    # 若設定檔沒有該token用途則預設10分鐘過期
    expired_time = time.time() + 10 * 60 if expire_length == None else time.time() + int(expire_length)
    # 使用 jwt 加密
    payload = data
    payload.update({
        'expired_time' : expired_time,
        'usage'        : usage
    })
    token = jwt.encode(payload, private_key, algorithm='RS512')
    return token, expired_time

def verify_token(token):
    # 若token不存在或是為空值
    if 'token' not in locals() or token is None or token == '':
        return False, dict()
    else:
        try:
            # 取得伺服器核發的公鑰（固定）
            public_key = Key().getPublicKey()
            payload = jwt.decode(token, public_key, algorithms=['RS512'])
            return True, payload
        # decode error or expired
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return False, dict()

def get_current_datetime(format=None):
    datetime_format = "%Y-%m-%d %H:%M:%S" if format == None else format
    return strftime(datetime_format, localtime())

def round_dict_value(data, decimal=1):
    result = dict()
    for k, v in data.items():
        if v is not None:
            result.update({k: round(float(v), decimal)})
        else:
            result.update({k: None})
    return result


def get_datetime_label():
    def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    # 今天日期
    today = date.today()
    # 最多獲取資料天數
    next_day = today + timedelta(1)
    time = datetime.min.time()
    today = datetime.combine(today, time)
    next_day = datetime.combine(next_day, time)

    dts = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in
        datetime_range(today, next_day,
        timedelta(minutes=1))]

    return dts

def get_accessory_publish_data(accessory, status):
    return {
        'datatime'  : get_current_datetime("%Y-%m-%d %H:%M:%S"),
        'accessory' : accessory,
        'status'    : status
    }

def tree_folder_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [tree_folder_dict(os.path.join(path, x)) for x in os.listdir\
(path)]
    else:
        d['type'] = "file"
    return d
