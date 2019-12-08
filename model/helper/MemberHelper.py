import bcrypt
from model.util.DBMgr import DBMgr

class MemberHelper():
    dbmgr = DBMgr()

    @staticmethod
    def check_duplicate_by_account(account):
        sql = "SELECT * FROM `iot`.`member` WHERE `member`.`account` = %(account)s"
        args = { 'account': account}

        status, row, result = MemberHelper.dbmgr.query(sql, args)

        if not status:
            result = {
                'error_type' : "DatabaseError",
                'error_msg'  : "[" + str(result[0]) + "]" + str(result[1]),
                'error_code' : 503
            }
            return False, result, 503
        elif row != 0:
            result = {
                'error_type' : "AccountDuplocatedError",
                'error_msg'  : "此帳號資料庫已經存在，請勿重複註冊",
                'error_code' : 400
            }
            return False, result, 400
        else:
            result = {
                'type' : "AccountPassVerify",
                'msg'  : "此帳號為新使用者，可以使用",
                'code' : 200
            }
            return True, result, 200

    @staticmethod
    def create(member):
        # 取得資料表欄位
        table_col = MemberHelper.dbmgr.get_db_column('iot', 'member')
        sql = MemberHelper.dbmgr.insert_sql('member', table_col, False)
        args = member.get_all_parameter()
        status, row, result = MemberHelper.dbmgr.insert(sql, args)

        # 看新增狀態
        if status:
            return True, {
                'type' : "AccountRegisterSuccess",
                'msg'  : "帳號新增至資料庫成功",
                'code' : 200
            }, 200
        else:
            return False, {
                'error_type' : "DatabaseError",
                'error_msg'  : "[" + str(result[0]) + "]" + str(result[1]),
                'error_code' : 500
            }, 500

    @staticmethod
    def verify(account, password):
        sql = "SELECT `password`, `identity` FROM `iot`.`member` WHERE `account`=%(account)s"
        args = { 'account': account}
        status, row, result = MemberHelper.dbmgr.query(sql, args)

        if not status:
            return False, {
                'error_type' : "DatabaseError",
                'error_msg'  : "[" + str(result[0]) + "]" + str(result[1]),
                'error_code' : 500
            }, 500
        # 發生未預期錯誤（帳號超過一個例外狀況）
        elif row > 1:
            return False, {
                'error_type' : "AccountMoreThanOneException",
                'error_msg'  : "資料庫存在該帳號之資料超過一筆異常",
                'error_code' : 500
            }, 500
        # 找不到帳號
        elif row == 0:
            return False, {
                'error_type' : "AccountVerifyError",
                'error_msg'  : "帳號不存在或密碼錯誤，請確認後重新輸入",
                'error_code' : 400
            }, 400
        # 自資料庫取回該帳號之加密密碼成功
        else:
            # 編碼成utf-8以進行檢查
            password = password.encode("utf-8")
            hash_password = result[0]["password"].encode("utf-8")

            # 嘗試進行bcrypt金鑰檢查
            if (bcrypt.checkpw(password, hash_password)):
                return True, {
                'type' : "AccountVerifySucess",
                'msg'  : "帳號密碼驗證成功",
                'code' : 200
            }, 200
            else:
                return False, {
                'error_type' : "AccountVerifyError",
                'error_msg'  : "帳號不存在或密碼錯誤，請確認後重新輸入",
                'error_code' : 400
            }, 400


