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

  toastr.success("標題", "內容內容內容內容內容內容內容內容內容內容內容內容內容內容內容", {
    "onclick": () => {
      console.log('yes')
    },
  });
  toastr.warning("標題", "內容內容內容內容內容內容內容內容內容內容內容內容內容內容內容", {
    "onclick": () => {
      console.log('yes')
    },
  });
  toastr.info("標題", "內容內容內容內容內容內容內容內容內容內容內容內容內容內容內容", {
    "onclick": () => {
      console.log('yes')
    },
  });
  toastr.error("標題", "內容內容內容內容內容內容內容內容內容內容內容內容內容內容內容", {
    "onclick": () => {
      console.log('yes')
    },
  });

  const socket = io.connect('/system');

  // Subscribe the Flask server publish data
  socket.on('sensor_data_pub_client', (data) => {
    console.log(data);
  });
})()
