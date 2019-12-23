from model.helper.SensorHelper import SensorHelper
from model.util.DBMgr import DBMgr

class MemberPreferenceHelper():
    # TODO: 新增預設檔案之前可能需要先檢查是否存在
    dbmgr = DBMgr()

    DEFAULT_ITEM = [item for item in SensorHelper.SENSOR_LIST if item['default']]

    @staticmethod
    def add_default_value(account):
        # TODO: 需要改成OO寫法
        sql = " INSERT INTO `iot`.`member_preference`(`account`, `item`, `min`, `max`) \
                VALUES(%(account)s, %(item)s, %(min)s, %(max)s)"
        args = list()

        for item in MemberPreferenceHelper.DEFAULT_ITEM:
            args.append( {
                'account'   : account,
                'min'       : item['min'],
                'max'       : item['max'],
                'item'      : item['id']
            })

        while True:
            status, row, result_id = MemberPreferenceHelper.dbmgr.insert(sql, args, multiple=True)
            if status:
                break
