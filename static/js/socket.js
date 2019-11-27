// 使用嚴格模式
"use strict";

(() => {
    const socket = io('//');

    socket.on('open', (data) => {
        console.log(data);
    });

    socket.emit('front-end-publish', { 'jello': '中文字體' });

    socket.on('front-end-response', (data) => {
        console.log(data);
    });
})()
