from datetime import datetime
from model.util.DBMgr import DBMgr
from model.util.KeyRSA import KeyRSA
from model.entity.RSA import RSA

class RSAHelper():
    dbmgr = DBMgr()

    @staticmethod
    def check_key_vaild(key_id, request_ip, usage):
        '''
        驗證金鑰有效性
        '''
        curr_datetime = datetime.now()
        sql = "SELECT * FROM `iot`.`rsa` WHERE `rsa`.`id` = %(id)s"
        args = { 'id': key_id}
        status, row, result = RSAHelper.dbmgr.query(sql, args)

        # Case 1： 資料庫檢索失敗
        if not status:
            result = {
                'error_type' : "DatabaseError",
                'error_msg'  : "[" + str(result[0]) + "]" + str(result[1]),
                'error_code' : 503
            }
        # Case 2： 金鑰超過一把（伺服器500發生未預期錯誤）
        elif row > 1:
            result = {
                'error_type' : "KeyMoreThanOne",
                'error_msg'  : "系統發生未預期錯誤，金鑰超過一把",
                'error_code' : 500
            }
        # Case 3： 金鑰不存在
        elif row == 0:
            result = {
                'error_type' : "KeyNotExist",
                'error_msg'  : "請求之金鑰不存在",
                'error_code' : 400
            }
        # Case 4： 金鑰與請求IP不相符（正確只會有一筆，直接取用list第一筆dict資料）
        elif result[0]['ip'] != request_ip:
            result = {
                'error_type' : "KeyNotMatchRequestIP",
                'error_msg'  : "請求之金鑰與IP位置不相符",
                'error_code' : 400
            }
        # Case 5： 金鑰請求與用途不相符
        elif result[0]['usage'] != usage:
            result = {
                'error_type' : "KeyNotMatchUsage",
                'error_msg'  : "請求之金鑰與金鑰用途不相符",
                'error_code' : 400
            }
        # Case 6： 金鑰已經過期
        elif result[0]['expire'] < curr_datetime:
            result = {
                'error_type' : "KeyExpired",
                'error_msg'  : "請求之金鑰已經失效",
                'error_code' : 400
            }
        # Case 7： 金鑰已經被使用
        elif result[0]['status'] == 1:
            result = {
                'error_type' : "KeyHasBeenUsed",
                'error_msg'  : "請求之金鑰已經被使用",
                'error_code' : 400
            }
        # Case 8： 金鑰驗證成功
        else :
            # 將金鑰重新封裝
            rsa_key = KeyRSA(result[0]['public_key'], result[0]['private_key'], result[0]['bits'])
            # 建立一個RSA物件回傳使用
            rsa = RSA(result[0]['id'], result[0]['usage'], result[0]['ip'], rsa_key, result[0]['create'], result[0]['expire'], result[0]['status'])

            return True, row, rsa

        return False, row, result
