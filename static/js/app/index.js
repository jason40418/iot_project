// 使用嚴格模式
"use strict";

(() => {
  const last_update = document.getElementById("real-time-id");
  const SLICK_SETTING = {
    slidesToScroll: 1,
    dots: true,
    autoplay: true,
    autoplaySpeed: 2000,
    mobileFirst: true,
    infinite: true,
    respondTo: 'window',
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: true,
          dots: true
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
    ]
  }

  document.addEventListener("DOMContentLoaded", (event) => {
    const socket = io.connect('/client');

    // Subscribe the Flask server publish data
    socket.on('sensor_data_pub_client', (payload) => {
      // 檢查目前也面數據資料是否和payload的編號是否相同或為舊資料
      if (Number(last_update.innerHTML) >= Number(payload['id'])) {
        // 不用更新
        console.log("[@index] Real-time data payload duplicate");
      }
      else {
        last_update.innerHTML = payload['id'];
        $.each(payload['data'], (key, value) => {
          if (value === null) {
            // 資料為null不用更新這部分
            console.log("[@index] Sensor data not exist")
          }
          else {
            // 如果資料存在則要更新
            $('#' + key + '-datetime').html(payload['datetime']);
            let original = $('#' + key + '-value').html();
            $('#' + key + '-value').html(value.toFixed(1));
            let change_result = calc_value_change(original, value)
            $('#' + key + '-value-change').html(change_result);
            blink_text('#' + key + '-value');
          }
        });
      }
    });

    // 產生slide show
    $('.real-time-data').slick(SLICK_SETTING);
  });

  let trace1 = {
    x: [1, 2, 3, 4],
    y: [10, 15, 13, 17],
    type: 'scatter'
  };

  let trace2 = {
    x: [1, 2, 3, 4],
    y: [16, 5, 11, 9],
    type: 'scatter'
  };

  let data = [trace1, trace2];

  let layout = {
    title: 'Responsive to window\'s size!',
    font: { size: 18 }
  };

  Plotly.newPlot('tester', data, layout, { responsive: true });
})()
