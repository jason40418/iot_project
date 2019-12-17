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

  var clean_status = (obj) => {
    STATUS.forEach((element) => {
      $(obj).removeClass('status-' + element);
    })
  }

  var update_status = (sensor, value) => {
    // 取回對應的狀態
    var [result, title, status] = get_sensor_status(sensor, value);
    // 如果檢驗狀態正確
    if (result) {
      // 更新標題
      $('#' + sensor + '-status').html(title);
      // 清除原先設定的狀態
      clean_status('#' + sensor + '-status-icon');
      // 設定新的狀態燈號
      $('#' + sensor + '-status-icon').addClass('status-' + status);
    }
  }

  document.addEventListener("DOMContentLoaded", (event) => {
    const socket = io.connect('/client');

    socket.on('connect', (payload) => {
      console.log(payload);
    });

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
            // 更新狀態
            update_status(key, value);
          }
        });
      }
    });

    // 將原本一開始的狀態更新上去
    $('.status-icon').each((idx, element) => {
      let icon_id = $(element).attr("id");
      let sensor = icon_id.split('-')[0];
      let value = Number($('#' + sensor + '-value').html())
      update_status(sensor, value);
    })
    // 產生slide show
    $('.real-time-data').slick(SLICK_SETTING);

  });
})()
