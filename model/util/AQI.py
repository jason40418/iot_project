import json
from model.helper.SensorHelper import SensorHelper

class AQI():

    # 取得最新資料
    sensor_result, sensor_data = SensorHelper.get_latest_data()

    def calc(self, data_list, data):
        sensor_level = self.__get_setting_file()
        total = 0
        score = 0

        for key in data_list:
            clean_key = key.replace('.', '').replace('+', '')

            if (key not in data) or (data[key] is None) or (data[key] == ""):
                pass
            else:
                # TODO: 處理可能不在的情況
                limit = sensor_level[clean_key]['limit']
                idx = 0

                for i in limit:
                    if data[key] < i:
                        break
                    else:
                        idx += 1

                item_score = sensor_level[clean_key]['level'][idx]['status']
                total += 4
                score += item_score

        # 避免除0
        total = 1 if total == 0 else total

        return score, total

    def get_latest_value(self, metrix):
        result, data = SensorHelper.get_latest_data()
        score, total = self.calc(metrix, data['data'])
        return score, total

    def __get_setting_file(self):
        result = dict()

        # 讀取設定檔案
        with open('static/json/sensor_level.json') as json_file:
            result = json.load(json_file)

        return result
