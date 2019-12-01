// 使用嚴格模式
"use strict";

(() => {
    const socket = io.connect('//');

    socket.on('test', (data) => {
        console.log(data);
    });

    socket.emit('test', { 'jello': '中文字體' });

    socket.on('front-end-response', (data) => {
        console.log(data);
    });
})()
