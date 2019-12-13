// 使用嚴格模式
"use strict";

(() => {
  const socket = io.connect('/client');

  // Subscribe the Flask server publish data
  socket.on('sensor_data_pub_client', (data) => {
    console.log(data);
  });
})()
