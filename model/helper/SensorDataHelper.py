from model.util.DBMgr import DBMgr

class SensorDataHelper():
    dbmgr = DBMgr()

    @staticmethod
    def get_sensor_from_db():
        sql = "SELECT * FROM `iot`.`sensor`"
        args = {}

        while True:
            status, row, record = SensorDataHelper.dbmgr.query(sql, args)
            if status:  break

        print(record)

        return record
