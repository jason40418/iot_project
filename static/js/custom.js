﻿// 使用嚴格模式
"use strict";

const HTTP_STATUS_CODES = {
  '200' : 'OK',
  '201' : 'Created',
  '202' : 'Accepted',
  '203' : 'Non-Authoritative Information',
  '204' : 'No Content',
  '205' : 'Reset Content',
  '206' : 'Partial Content',
  '300' : 'Multiple Choices',
  '301' : 'Moved Permanently',
  '302' : 'Found',
  '303' : 'See Other',
  '304' : 'Not Modified',
  '305' : 'Use Proxy',
  '307' : 'Temporary Redirect',
  '400' : 'Bad Request',
  '401' : 'Unauthorized',
  '402' : 'Payment Required',
  '403' : 'Forbidden',
  '404' : 'Not Found',
  '405' : 'Method Not Allowed',
  '406' : 'Not Acceptable',
  '407' : 'Proxy Authentication Required',
  '408' : 'Request Timeout',
  '409' : 'Conflict',
  '410' : 'Gone',
  '411' : 'Length Required',
  '412' : 'Precondition Failed',
  '413' : 'Request Entity Too Large',
  '414' : 'Request-URI Too Long',
  '415' : 'Unsupported Media Type',
  '416' : 'Requested Range Not Satisfiable',
  '417' : 'Expectation Failed',
  '500' : 'Internal Server Error',
  '501' : 'Not Implemented',
  '502' : 'Bad Gateway',
  '503' : 'Service Unavailable',
  '504' : 'Gateway Timeout',
  '505' : 'HTTP Version Not Supported'
};

/**
 * @description 禁止表單自動轉頁送出，並且可客製化自己的判斷函數
 * @param {*} object
 * @param {*} action
 *
 * @version 1.0.0
 * @author Jason Lin
 *
 * @requires
 */
var disable_submit_form = (object, action) => {
  $('#' + object).validator().on('submit', (e) => {
    // 表單送出未通過資料驗證
    if (e.isDefaultPrevented()) {
      // handle the invalid form...
      console.log('error')
    } else {
      e.preventDefault();
      action();
    }
    return false;
  });
}

var current_time = () => {
  Date.prototype.toIsoString = function () {
    var tzo = -this.getTimezoneOffset(),
      dif = tzo >= 0 ? '+' : '-',
      pad = function (num) {
        var norm = Math.floor(Math.abs(num));
        return (norm < 10 ? '0' : '') + norm;
      };
    return this.getFullYear() +
      '-' + pad(this.getMonth() + 1) +
      '-' + pad(this.getDate()) +
      'T' + pad(this.getHours()) +
      ':' + pad(this.getMinutes()) +
      ':' + pad(this.getSeconds()) +
      dif + pad(tzo / 60) +
      ':' + pad(tzo % 60);
  }

  let date = new Date();
  let result = date.toIsoString().slice(0, 19).replace('T', ' ');

  return result;
}

var get_date_time = (data) => {

  let date = new Date(data);
  let result = date.toISOString().slice(0, 19).replace('T', ' ');

  return result;
}

/**
 * 檢驗是否是function
 * @param {*} func
 */
var is_function = (func) => {
  return func && {}.toString.call(func) === '[object Function]';
}

var number_increase = () =>{
  $('.number').each(function () {
    if ($(this).text() === '--.-') {
      console.log('NaN')
    }
    else {
      $(this).prop('Counter', 0).animate({
        Counter: Number($(this).text())
      }, {
        duration: 2000,
        easing: 'swing',
        step: function (now) {
          $(this).text(Math.ceil(now));
          $(this).number(true, 1);
        }
      });
    }
  });
}

/**
 * 使用jquery-confirm跳出
 * @param {*} title
 * @param {*} message
 * @param {*} icon
 * @param {*} button
 */
var alert = (title, message, icon, button) => {
  $.alert({
    theme: 'modern',
    icon: icon,
    type: 'red',
    animation: 'scale',
    title: title,
    content: message,
    buttons: button
  });
}

/**
 *
 * @param {*} request_type
 * @param {*} request_url
 * @param {*} request_data
 * @param {*} button
 */
var api_request = (request_type, request_url, request_data, button, promp=[true, true]) => {
  let api_result = false;
  let api_response = new Object();
  $.ajax({
    type: request_type,
    url: request_url,
    data: JSON.stringify(request_data),
    async: false,
    crossDomain: true,
    cache: false,
    dataType: 'json',
    contentType: 'application/json',
    timeout: 5000})
  .done((response, test_status, xhr) => {
    // 紀錄API請求為成功
    api_result = true;
    api_response = response;
    let alert_msg = "";
    // 確認Response包含所需要的key值以正常顯示
    if (typeof response === 'undefined') {
      alert_msg = "[" + xhr.status + "]" + xhr.statusText;
    }
    else if ('code' in response && 'type' in response && 'msg' in response) {
      alert_msg = "[" + response.code + "]" + "[" + response.type + "]" + "<br />" + response.msg;
    }
    else {
      alert_msg = "[" + xhr.status + "]" + xhr.statusText;
    }

    if (promp[0]) {
      // 跳出提示視窗
      $.alert({
        theme: 'modern',
        icon: 'fa fa-check-circle',
        type: 'green',
        btnClass: 'btn-green',
        animation: 'scale',
        title: '成功',
        content: alert_msg,
        buttons: button['2XX']
      });
    }
  })
  .fail((xhr, type, message) => {
    let response = xhr.responseJSON;
    let alert_msg = "";
    api_response = (typeof response === 'undefined') ? api_response : response;
    // 確認Response包含所需要的key值以正常顯示
    if (typeof response === 'undefined') {
      alert_msg = "[" + xhr.status + "]" + message;
    }
    else if ('error_code' in response && 'error_type' in response && 'error_msg' in response) {
      alert_msg = "[" + response.error_code + "]" + "[" + response.error_type + "]" + "<br />" + response.error_msg;
    }
    else {
      console.log('test')
      alert_msg = "[" + xhr.status + "]" + message;
    }

    if (promp[1]) {
      // 使用者網路連線異常或伺服器無法進行連線
      if (xhr.status == 0) {
        alert('服務無法提供', '請確認網路連線是否正常或伺服器可能現在無法提供服務！', 'fa fa-chain-broken', { 確認: () => { }});
      }
      // 使用者端問題（4XX）
      else if (xhr.status >= 400 & xhr.status < 500) {
        $.alert({
          theme: 'modern',
          icon: 'fa fa-times',
          type: 'red',
          btnClass: 'btn-red',
          animation: 'scale',
          title: '錯誤',
          content: alert_msg,
          buttons: button['4XX']
        });
      }
      // 伺服器端問題（5XX）
      else if (xhr.status >= 500 & xhr.status < 600) {
        $.alert({
          theme: 'modern',
          icon: 'fa fa-server',
          type: 'red',
          btnClass: 'btn-red',
          animation: 'scale',
          title: '錯誤',
          content: alert_msg + "<br />" + "請將錯誤代碼與訊息聯絡管理員",
          buttons: button['5XX']
        });
      }
    }
  });

  return [api_result, api_response];
}

/**
 *
 * @param {*} icon
 * @param {*} url
 * @param {*} title
 * @param {*} color
 * @param {*} button
 * @param {*} content_ready
 * @param {*} close_icon
 */
var prompt_info = (icon, url, title, color, button, content_ready="", close_icon=true) => {
  $.confirm({
    theme: 'material',
    icon: icon,
    columnClass: 'medium',
    animation: 'scale',
    closeIcon: close_icon,
    closeIconClass: 'fa fa-close',
    type: color,
    title: title,
    content: url,
    onContentReady: function () {
      if (is_function(content_ready)) {
        content_ready();
      }
    },
    draggable: false,
    buttons: button
  });
}

var calc_value_change = (last, curr) => {
  let change = Number();
  if (isNaN(last)) { change = 0.0;}
  else{ change = Number(curr) - Number(last);}

  let sign = "";
  let color = "";
  if (change > 0)       { sign = "▲";   color = "#F0382B";}
  else if (change < 0)  { sign = "▼";   color = "#69F25C";}
  else                  { sign = "-";   color = "#6B6E6A";}

  return '<span style="color:' + color + ';">' + sign + ' ' + String(Math.abs(Number(change)).toFixed(1)) + '</span>';
}

/**
 * 函數需要使用async，內部使用await
 * @param {*} ms
 */
var sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 *
 * @param {*} obj
 * reference: http://jsfiddle.net/M4Fcd/186/
 */
var blink_text = (obj) => {
  $(obj).each(function() {
    var elem = $(this);
    var count = 1;
    var intervalId = setInterval(function() {
        if (elem.css('visibility') == 'hidden') {
            elem.css('visibility', 'visible');
            if (count++ === 3) {
                clearInterval(intervalId);
            }
        } else {
            elem.css('visibility', 'hidden');
        }
    }, 200);
  });
}

var get_status_code_by_value = (object, value) => {
  return Object.keys(object).find(key => (object[key]).toLowerCase() === value.toLowerCase());
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

var update_curr_status = () => {
  $('.status-icon').each((idx, element) => {
    let icon_id = $(element).attr("id");
    let sensor = icon_id.split('-')[0];
    let value = Number($('#' + sensor + '-value').html())
    update_status(sensor, value);
  });
}

var getCookie = (name) => {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

var get_cookie_data = (key) => {
  let pref = (getCookie(key) == null) ?  "" : getCookie(key);
  let pref_obj = new Object();
  if (pref != "") {
    pref = pref.replace(/\\054/g, ',');
    pref_obj = JSON.parse(JSON.parse(pref));
  }
  return pref_obj;
}
