from model.util.DBMgr import DBMgr

class SensorHelper():
    dbmgr = DBMgr()
    SENSOR_LIST = [
        {
            'id'   : "temperature",
            'icon' : "fa-thermometer-half",
            'name' : "溫度（Temperature）",
            'unit' : "°C"
        },
        {
            'id'   : "humidity",
            'icon' : "fa-tint",
            'name' : "濕度（Humidity）",
            'unit' : "%"
        },
    ]
    # TODO: 若資料庫出錯是否要印出或做其他處置
    @staticmethod
    def get_new_record_id(promotor='system'):
        sql = "INSERT INTO `iot`.`record`(`promotor`) VALUES(%(promotor)s)"
        args = { 'promotor': promotor}
        while True:
            status, row, result_id = SensorHelper.dbmgr.insert(sql, args)
            if status:
                break
        return result_id

    @staticmethod
    def insert_sensor_data(data, record_id):
        sql = "INSERT INTO `iot`.`data`(`record_id`, `item`, `value`) VALUES(%(record_id)s, %(sensor)s, %(value)s)"
        args = list()
        # 進來的資料為{sensor: value}
        for k, v in data.items():
            args.append({'sensor': k, 'value': v, 'record_id': record_id})
        while True:
            status, row, result_id = SensorHelper.dbmgr.insert(sql, args, multiple=True)
            if status:
                break
            else:
                print(result_id)
        print("[@SensorHelper] Insert all this record data into db finish.")

    @staticmethod
    def update_fail_list(data_list, record_id):
        sql = "UPDATE `iot`.`record` SET `fail_list`=%(fail_list)s WHERE `record`.`id`=%(id)s"
        args = {
            'fail_list': SensorHelper.dbmgr.list_to_string(data_list),
            'id'       : record_id
        }
        while True:
            status, row, result = SensorHelper.dbmgr.update(sql, args)
            if status:
                break
        print("[@SensorHelper] Update fail sensor list finish.")

    @staticmethod
    def get_latest_data():
        sql = "SELECT * FROM `iot`.`record` ORDER BY `record`.`id` DESC LIMIT 1"
        args = {}

        while True:
            status, row, record = SensorHelper.dbmgr.query(sql, args, fetch='one')
            if status:  break

        # 資料庫無任何資料
        if row == 0:
            return False, {}
        else:
            # 取得資料庫內所有該次監測的資料
            record_id = record['id']
            sql = "SELECT * FROM `iot`.`data` WHERE `data`.`record_id`=%(id)s"
            args = { 'id': record_id}

            data_dict = dict()
            while True:
                status, row, data = SensorHelper.dbmgr.query(sql, args)
                if status:  break

            for datum in data:
                data_dict.update({datum['item']: round(float(datum['value']), 1)})

            # 組回原本格式
            result = {
                'id': record_id,
                'datetime':  record['datetime'],
                'fail' : SensorHelper.dbmgr.string_to_list(record['fail_list']),
                'data': data_dict
            }
            return True, result
