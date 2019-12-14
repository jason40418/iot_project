const STATUS = ['green', 'yellow', 'orange', 'red', 'purple'];
var sensor_level;

// TODO: 萬一沒抓到這個檔案
$.ajax({
  type: "GET",
  dataType: "json",
  url: "/static/json/sensor_level.json",
  async: false,
  crossDomain: true,
  cache: false,
})
.done((response, test_status, xhr) => {
  sensor_level = response;
});

var get_sensor_status = (sensor, value) => {
  // Sensor不在變數裡面
  if (!(sensor in sensor_level)) {
    console.log("This sensor not exist!");
  }
  else {
    // 檢查邊界、mapping的key是否存在
    if ('limit' in sensor_level[sensor] && 'level' in sensor_level[sensor]) {
      let limit = sensor_level[sensor]['limit'];
      let level = sensor_level[sensor]['level']
      // 檢查是否有設定邊界
      // TODO: 應該先檢查兩個物件型態是否正確、檢查兩個長度是否相同
      if (limit.length === 0 || Object.keys(level).length === 0) {
      }
      else {
        let i = 0;
        limit.forEach((element) => {
          if (value >= element) {  i+=1;}
        });

        // TODO: 檢查取回的資料格式是否正確
        let title = level[i]['title'];
        let status = level[i]['status'];
        return [true, title, STATUS[status]];
      }
    }
    else {
      console.log("Some key not exist!")
    }
  }
  return [false, "", ""];
}
