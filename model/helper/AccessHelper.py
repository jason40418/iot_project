import datetime
from model.util.DBMgr import DBMgr

class AccessHelper():
    dbmgr = DBMgr()

    @staticmethod
    def get_by_name(account):
        sql = " SELECT * \
                FROM `iot`.`access` \
                WHERE `access`.`account` = %(account)s \
                ORDER BY `access`.`id` DESC"
        args = { 'account': account}

        while True:
            status, row, data = AccessHelper.dbmgr.query(sql, args)
            if status:  break

        if row == 0:
            return False, {}
        elif row == 1:
            return True, data[0]
        # 為系統發生例外狀況
        else:
            return True, data[0]

    @staticmethod
    def get_records_by_name(account):
        sql = " SELECT * \
                FROM `iot`.`access_record` \
                WHERE `access_record`.`account` = %(account)s \
                ORDER BY `access_record`.`id` DESC"
        args = { 'account': account}

        while True:
            status, row, data = AccessHelper.dbmgr.query(sql, args)
            if status:  break

        return status, row, data

    @staticmethod
    def entry(account):
        sql = "INSERT INTO `iot`.`access`(`access`.`account`) VALUES(%(account)s)"
        args = { 'account': account}

        while True:
            status, row, result_id = AccessHelper.dbmgr.insert(sql, args, multiple=False)
            if status:
                break

    @staticmethod
    def delete(account):
        sql = "DELETE FROM `iot`.`access` WHERE `access`.`account` = %(account)s"
        args = { 'account': account}

        while True:
            status, row, result_id = AccessHelper.dbmgr.delete(sql, args)
            if status: break
    @staticmethod
    def add_record(account, entry, exit):
        sql = " INSERT INTO `iot`.`access_record`(`access_record`.`account`, `access_record`.`entry`, `access_record`.`exit`) \
                VALUES(%(account)s, %(entry)s, %(exit)s)"
        args = {
            'account': account,
            'entry': entry,
            'exit': exit,
        }

        while True:
            status, row, result_id = AccessHelper.dbmgr.insert(sql, args, multiple=False)
            if status:
                break

    @staticmethod
    def exit(account, entry_dt,  trigger=None):
        entry_dt_str = entry_dt.isoformat(' ')

        if trigger == 'system':
            years = entry_dt.year
            months = entry_dt.month
            days = entry_dt.day
            exit_dt = datetime.datetime(years, months, days, 23, 59, 59)
            exit_dt_str = exit_dt.isoformat(' ')

        else:
            exit_dt_str = datetime.datetime.today().isoformat(' ')

        AccessHelper.add_record(account, entry_dt_str, exit_dt_str)
        AccessHelper.delete(account)
