import datetime
import pandas as pd
from model.util.DBMgr import DBMgr

class SensorHelper():
    dbmgr = DBMgr()
    SENSOR_LIST = [
        {
            'id'      : "temperature",
            'icon'    : "fa-thermometer-half",
            'name'    : "溫度",
            'en_name' : "Temperature",
            'unit'    : "°C"
        },
        {
            'id'      : "humidity",
            'icon'    : "fa-tint",
            'name'    : "濕度",
            'en_name' : "Humidity",
            'unit'    : "%"
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

    @staticmethod
    def get_sensor_his_data(sensor, day=30, is_resample=True, remain=-1):
        # 今天日期
        today = datetime.date.today()
        # 最多獲取資料天數
        limit_day = today - datetime.timedelta(day)
        # 取得符合監測記錄
        sql = "SELECT * FROM `iot`.`record` WHERE `record`.`datetime` >= %(date)s ORDER BY `record`.`id` ASC LIMIT 1"
        args = { 'date': limit_day.strftime("%Y-%m-%d")}
        status, row, record = SensorHelper.dbmgr.query(sql, args, fetch='one')
        day_info = {
            'start': limit_day.strftime("%Y-%m-%d"),
            'end': today.strftime("%Y-%m-%d")
        }
        #
        if status and row != 0:
            sql = " SELECT  `record`.`datetime`, `data`.`value` \
                    FROM    `iot`.`record`, `iot`.`data` \
                    WHERE   `record`.`id` = `data`.`record_id` AND `data`.`record_id` >= %(record_id)s AND `data`.`item` = %(sensor)s"
            args =  {
                'record_id' : record['id'],
                'sensor'    : sensor
            }
            status, row, data = SensorHelper.dbmgr.query(sql, args)

            # 成功取回至少一筆資料
            if status and row != 0:
                for datum in data:
                    try:
                        datum['value'] = round(float(datum['value']), 3)
                    except:
                        datum['value'] = None

                df, df_h = SensorHelper.data_convert_to_dataframe(data, is_resample=is_resample)

                # 判斷最後df要保留多少長度資料
                if remain > 0 and len(df.index) >= remain:
                    df = df[0:remain]

                return True, df, df_h, row, day_info
            # 失敗或沒有取得資料
            else:
                return False, pd.DataFrame(), pd.DataFrame(), 0, day_info
        # 資料庫沒有任何紀錄
        else:
            return False, pd.DataFrame(), pd.DataFrame(), 0, day_info

    @staticmethod
    def data_convert_to_dataframe(data, resample='60Min', sort=False, is_resample=True):
        # TODO: 檢查參數是否型態與格式正確
        df = pd.DataFrame(data)
        df.set_index("datetime" , inplace=True)

        # 新增統計高低數值欄位
        df['high'] = df['value']
        df['low'] = df['value']

        if is_resample:
            # 重新進行取樣
            df = df.resample(resample).agg({
                'high'  : 'max',
                'low'   : 'min',
                'value' : 'mean'
            })
            df = df.asfreq(resample)

            # 以小時進行合併
            s_low = df['low'].groupby(df['low'].index.hour).min()
            s_high = df['high'].groupby(df['high'].index.hour).max()
            s_mean = df['value'].groupby(df['value'].index.hour).mean()
            df_h = pd.concat([s_low, s_high, s_mean], axis=1)
        else:
            # 以分鐘進行合併
            s_low = df['low'].groupby(df['low'].index.minute).min()
            s_high = df['high'].groupby(df['high'].index.minute).max()
            s_mean = df['value'].groupby(df['value'].index.minute).mean()
            df_h = pd.concat([s_low, s_high, s_mean], axis=1)

        # 取小數點至第二位，並且重設index
        df = df.round(2).reset_index()
        df['datetime'] = df['datetime'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        df = df.sort_values(by=["datetime"], ascending=[sort])
        df = df.dropna()

        df_h = df_h.round(2).reset_index()
        df_h = df_h.dropna()

        return df, df_h

    @staticmethod
    def get_statist_data(sensor, period, header):
        '''
        不能傳入年，要使用要用relative
        '''
        # TODO: 若傳入資料格式錯誤之異常處理（包含key值）
        time_idx = ['hours', 'minutes', 'seconds']
        result = list()
        for item in period:
            # 判斷是否要抓取到時間部分
            get_all = False
            if 'all' in item.keys():
                get_all = True
            elif list(set(time_idx) & set(item.keys())):
                today = datetime.datetime.now()
                limit_day = (today - datetime.timedelta(**item)).strftime("%Y-%m-%d %H:%M:%S")
                today = today.strftime("%Y-%m-%d %H:%M:%S")
            else:
                today = datetime.date.today()
                limit_day = (today - datetime.timedelta(**item)).strftime("%Y-%m-%d")
                today = today.strftime("%Y-%m-%d")

            # 使用SQL指令取回資料庫筆數和平均數
            # 取得符合監測記錄
            if get_all:
                sql = "SELECT * FROM `iot`.`record` ORDER BY `record`.`id` ASC LIMIT 1"
            else:
                sql = "SELECT * FROM `iot`.`record` WHERE `record`.`datetime` >= %(date)s ORDER BY `record`.`id` ASC LIMIT 1"
            args = { 'date': limit_day}
            status, row, record = SensorHelper.dbmgr.query(sql, args, fetch='one')
            # 將該筆之日期資訊儲存
            temp_result = { 'start': limit_day, 'end':   today}

            if status and row != 0:
                sql = " SELECT      SUM(`data`.`value`) as `sum`, COUNT(`data`.`value`) as `count`, SUM(`data`.`value`)/COUNT(`data`.`value`) as `avg` \
                        FROM        `iot`.`record`, `iot`.`data` \
                        WHERE       `record`.`id` = `data`.`record_id` AND `data`.`record_id` >= %(record_id)s AND `data`.`item` >= %(sensor)s\
                        GROUP BY    `data`.`item`"
                args =  {
                    'record_id' : record['id'],
                    'sensor'    : sensor
                }
                status, row, data = SensorHelper.dbmgr.query(sql, args, fetch='one')

                # 成功取回至少一筆資料
                if status and row != 0:
                    temp_result.update({
                        'sum': round(data['sum'], 2),
                        'count': int(data['count']),
                        'avg': round(data['avg'], 2)
                    })
                # 失敗或沒有取得資料
                else:
                    temp_result.update({
                        'sum': 0.00,
                        'count': 0,
                        'avg': 0.00
                    })
            # 資料庫沒有任何紀錄
            else:
                temp_result.update({
                    'sum': 0.00,
                    'count': 0,
                    'avg': 0.00
                })

            result.append(temp_result)

        return header, result
