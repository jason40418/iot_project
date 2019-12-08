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


