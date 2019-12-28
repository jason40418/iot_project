from model.helper.AccessHelper import AccessHelper
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

    @staticmethod
    def get_by_account(account):
        sql = "SELECT * FROM `iot`.`member_preference` WHERE `member_preference`.`account` = %(account)s"
        args = { 'account'   : account}

        item_list = list()

        while True:
            status, row, result = MemberPreferenceHelper.dbmgr.query(sql, args)
            if status: break

        for i in result:
            item_list.append(i['item'])

        return result, item_list

    @staticmethod
    def calc_avg_pref_value():
        """ Use for to calculate the averger value of preference in this room
        """
        # 取得目前在環境中的人員數量
        status, row, data = AccessHelper.get_all()

        people = [i['account'] for i in data] if status else list()
        result = dict()

        for item in MemberPreferenceHelper.DEFAULT_ITEM:
            if not status or row <= 0:
                result.update({
                    item['id']: {
                        'min': item['min'],
                        'max': item['max'],
                    }
                })
            else:
                sql = " SELECT  * \
                        FROM    `iot`.`member_preference` \
                        WHERE   `member_preference`.`item`=%(item)s AND \
                                `member_preference`.`account` in %(people)s"
                args = {
                    'item': item['id'],
                    'people': tuple(people)
                }

                while True:
                    status, row, data = MemberPreferenceHelper.dbmgr.query(sql, args)
                    if status: break

                # 判斷是否有抓取到該項目偏好設定檔案
                if row == 0:
                    result.update({
                        item['id']: {
                            'min': item['min'],
                            'max': item['max'],
                        }
                    })
                else:
                    min_value = float(sum(d['min'] for d in data)) / len(data)
                    max_value = float(sum(d['max'] for d in data)) / len(data)
                    result.update({
                        item['id']: {
                            'min': round(min_value, 2),
                            'max': round(max_value, 2),
                        }
                    })

        return result, people, len(people)

    @staticmethod
    def edit(args):
        sql = " UPDATE  `iot`.`member_preference` \
                SET     `member_preference`.`min` = %(min)s, \
                        `member_preference`.`max` = %(max)s \
                WHERE   `member_preference`.`item` = %(item)s AND \
                        `member_preference`.`account` = %(account)s"

        while True:
            status, row, result = MemberPreferenceHelper.dbmgr.update(sql, args, multiple=True)
            if status: break

        return row
