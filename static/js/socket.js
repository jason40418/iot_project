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
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }

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
    console.log(payload);
  })
})()
