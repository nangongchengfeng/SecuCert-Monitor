function getCPUData() {
    // 使用原生 JavaScript 发送 Ajax 请求
    // var xhr = new XMLHttpRequest();
    // xhr.onreadystatechange = function () {
    //     if (xhr.readyState === 4 && xhr.status === 200) {
    //         var cpuPercent = JSON.parse(xhr.responseText).cpu_percent;
    //         updateChart_cpu(cpuPercent); // 调用更新图表的函数
    //     }
    // };
    // xhr.open('GET', '/get_cpu_data', true);
    // xhr.send();

    // 使用 jQuery 发送 Ajax 请求
    $.ajax({
        url: '/get_cpu_data',
        dataType: 'json',
        type: 'GET',
        success: function (data) {
            var cpuPercent = data.cpu_percent;
            updateChart_cpu(cpuPercent); // 调用更新图表的函数
        },
        error: function (xhr, status, error) {
            console.log('获取数据失败');
        }
    });
}

// 定义函数，更新图表数据并重新渲染图表
function updateChart_cpu(cpuPercent) {
    option_cpu.series[0].data[0].value = cpuPercent;
    myChart_CPU.setOption(option_cpu);
}

getCPUData();
setInterval(getCPUData, 5000);