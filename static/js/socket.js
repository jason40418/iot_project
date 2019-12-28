/**
 * @description: 本檔案用於用於處理伺服器發布給用戶端之訊息，並使其產生浮動視窗於每個頁面
 */

(() => {
  // 使用嚴格模式
  "use strict";
  toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "10000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }

  const sensor = sensor_level;
  console.log(sensor);

  const socket = io.connect('/system');

  // Subscribe the Flask server publish data
  socket.on('face_identify_pub_system', (payload) => {
    console.log(payload);
    // 處理進入環境事件
    if (payload['data']['category'] == 'entry') {
      $.each(payload['data']['people'], async function (key, value) {
        toastr.success('[人臉辨識 Face Identify]', value + '已經進入該環境', () => {
        });
        await sleep(1000);
      });
    }
    // 處理離開環境事件
    else if (payload['data']['category'] == 'exit') {
      $.each(payload['data']['people'], async function (key, value) {
        toastr.success('[人臉辨識 Face Identify]', value + '已經離開該環境', () => {
        });
        await sleep(1000);
      });
    }
  });

  socket.on('sensor_data_pub_system', (payload) => {
    let [api_result, api_response] = api_request('GET', '/api/member/pref_avg', {}, {}, [false, false]);
    let obj = new Object();

    if (api_result) obj = api_response['data'];

    $.each(payload['data'], function (key, value) {
      sleep(1000 * Math.floor((Math.random() * 5) + 1)).then(() => {
        if (value === undefined || value === null) {
        }
        else {
          let clean_key = key.replace('.', '').replace('+', '');
          let title = sensor[clean_key]['name'] + ' ' + clean_key;

          // 有偏好設定
          if (key in obj) {
            let range = '(' + obj[key]['min'] + '~' + obj[key]['max'] + ')';

            if (value < obj[key]['min'])        toastr.error('[' + title + ']', '" ' + value + ' "低於範圍數值' + range, () => {});
            else if (value > obj[key]['max'])   toastr.error('[' + title + ']', '" ' + value + ' "超過範圍數值' + range, () => {});
            else                                console.log('[' + title + ']', '" ' + value + ' "位於正常範圍' + range);
          }
          // 無偏好設定
          else {
            let [status, content, style] = get_sensor_status(clean_key, value);

            if (status) {
              let key = STATUS.indexOf(style);
              console.log(key);
              if (key > 2)        toastr.error('[' + title + ']', '目前數值" ' + value + ' "' + content + '，請遠離！', () => {});
              else if (key > 0)   toastr.warning('[' + title + ']', '目前數值" ' + value + ' "' + content + '，請多加留意！', () => {});
              else if (key == 0)  console.log('[' + title + ']', '目前數值" ' + value + ' "，位於正常範圍！');
            }
            else {

            }
          }
        }
      });
    });
  })
})()
