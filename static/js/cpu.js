var myChart_CPU = echarts.init(document.getElementById('cpu'));
// 指定图表的配置项和数据
var option_cpu = {
    tooltip: {
        formatter: '{a} <br/>{b} : {c}%'
    },
    series: [
        {
            name: 'CPU',
            type: 'gauge',
            progress: {
                show: true
            },
            detail: {
                valueAnimation: true,
                formatter: '{value}'
            },
            data: [
                {
                    value: '0',
                    name: 'CPU使用率'
                }
            ]
        }
    ]
};


// 使用刚指定的配置项和数据显示图表。
myChart_CPU.setOption(option_cpu);
// 使用 setInterval 定时刷新数据
// setInterval(getCPUData, 5000); // 每5秒刷新一次数据