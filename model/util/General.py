import ast, json
from functools import wraps
from flask import request
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as ORI_RSA
from Crypto.Hash import SHA256
from base64 import b64decode

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

def public_key_require_page(usage, expire_para):
    # 需要增加產生RSA key
    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            # 取得RSA過期時間設定
            expire = Config().getValue('expire', expire_para)
            # 請求資源的IP位置
            request_ip = request.remote_addr
            rsa_key = KeyRSA()
            rsa = RSA(usage, request_ip, rsa_key, expire)

            data = {'id': rsa.get_rsa_key_id(), 'public_key': rsa_key.get_public_key()}

            return f(data)

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

            # 金鑰
            if rsa_key_exist:
                # 詳細金鑰
                rsa_key_info = decode_result.get_parameter()

                try:
                    # 設定私鑰
                    private_key = ORI_RSA.importKey(rsa_key_info['private_key'])
                    # 設定RSA私鑰與hash演算法組合
                    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
                    try:
                        # 解密資料
                        decrypted_message = cipher.decrypt(b64decode(data[encrypt_data_key]))
                        # 將Byte轉換成JSON格式的dict
                        decode_result, decrypted_message_dict = convert_byte_to_dict(decrypted_message)
                        # 回傳最終解析結果
                        return f(decode_result, decrypted_message_dict)
                    # 資料解密錯誤
                    except Exception as e:
                        decode_result = {
                            'error_type' : "KeyDecodeError",
                            'error_msg'  : "請求之內容無法進行解密",
                            'error_code' : 400
                        }
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
            else:
                # 金鑰失敗接續處理位置
                pass

            return f(False, decode_result)
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

