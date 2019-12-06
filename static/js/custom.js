// 使用嚴格模式
"use strict";

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

var alert = (title, message) => {
  $.alert({
    theme: 'modern',
    icon: 'fa fa-minus-circle',
    type: 'red',
    animation: 'scale',
    title: title,
    content: message
  });
}
