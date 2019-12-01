// 使用嚴格模式
"use strict";

(() => {
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
