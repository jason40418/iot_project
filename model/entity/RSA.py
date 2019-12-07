from Crypto.PublicKey import RSA
from datetime import datetime, timedelta
from time import localtime, strftime
import random

from model.util.Overload import MultipleMeta
from model.util.Config import Config
from model.util.DBMgr import DBMgr
from model.util.KeyRSA import KeyRSA

''' RSA Status說明
0 - 金鑰未被使用
1 - 金鑰已被使用
'''
class RSA(metaclass=MultipleMeta):
    def __init__(self, rsa_id:str, usage:str, ip:str, rsa_key:KeyRSA, create:datetime, expire:datetime, status: int):
        self.__rsa_id = rsa_id
        self.__usage = usage
        self.__ip = ip
        self.__rsa_key = rsa_key
        self.__create = create
        self.__expire = expire
        self.__status = status
        self.__cfg = Config()
        self.__dbmgr = DBMgr()

    def __init__(self, usage:str, ip:str, rsa_key:KeyRSA, expire:str):
        self.__usage = usage
        self.__ip = ip
        self.__rsa_key = rsa_key
        self.__create = datetime.now()
        self.__expire = self.__create + timedelta(seconds=int(expire))
        self.__status = 0
        self.__cfg = Config()
        self.__dbmgr = DBMgr()
        self.__rsa_id = self.__insert_to_db()

    def __gen_rsa_key_id(self):
        # 取得現在日期
        time = strftime("%Y%m%d%H%M%S", localtime())

        # 產生三位數隨機亂碼
        rand = random.randint(0, 999)
        # 不足位數前方補0
        rand = "%03d" % rand

        return (time + rand)

    def __insert_to_db(self):

        while 1:
            # 產生一組隨機號碼
            key_id = self.__gen_rsa_key_id()

            # 檢查是否有重複
            if not self.__check_duplicate(key_id):
                break

        self.__rsa_id = key_id
        column = self.__dbmgr.get_db_column('iot', 'rsa')
        sql = self.__dbmgr.insert_sql('rsa', column, True)
        args = self.get_parameter()
        result, row, error_msg = self.__dbmgr.insert(sql, args)

        return key_id

    def __check_duplicate(self, key_id):
        if(self.__dbmgr.conn()):
            try:
                with self.__dbmgr.cursor() as cursor:
                    sql = "SELECT * FROM `iot`.`rsa` WHERE `id` = %(id)s"
                    args = { 'id': key_id}

                    num_of_rows = int(cursor.execute(sql, args))
                    result = cursor.fetchall()
                    self.__dbmgr.commit()

            except self.__dbmgr.mysql_error() as e:
                print('[@RSA] 【{}】{!r}'.format(e.args[0], e.args[1]))

        else:
            print("[@RSA] Fails to connect to MySQL Server!!")

        self.__dbmgr.close()

        return True if num_of_rows != 0 else False

    def get_parameter(self):
        return {
            'usage'       : self.__usage,
            'ip'          : self.__ip,
            'bits'        : self.__rsa_key.get_bits(),
            'public_key'  : self.__rsa_key.get_public_key(),
            'private_key' : self.__rsa_key.get_private_key(),
            'create'      : self.__create,
            'expire'      : self.__expire,
            'status'      : 0,
            'id'          : self.__rsa_id
        }

    def __remove_all_expire_keys(self):
        sql = "DELETE FROM  `iot`.`rsa` WHERE `iot`.`expire` < '%(date_time)s';"
        args = { 'date_time': datetime.datetime.now()}
        status, row, result = self.__dbmgr.delete(sql, args)

    def get_rsa_key_id(self):
        return self.__rsa_id
