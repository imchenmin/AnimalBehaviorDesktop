<template lang="">
    <StepControl :_id="exp_id" active="2"></StepControl>
    <!-- <el-button v-if="displayChart"  value="查看结果" id="showresult" @click="embyPot">查看结果</el-button> -->
    <el-button  value="查看结果" id="showresult" @click="run_analysis" status="finish">分析</el-button>
    <el-button  value="查看结果" id="showresult" @click="playVideo" ref="previewBtn">打开相机</el-button>
    <video ref="videoPlayerTop" class="video-js"></video>
    <!-- <video ref="videoPlayerSide" class="video-js"></video> -->



    <v-chart v-if="displayChart" class="chart" :option="option" />
</template>
<script lang="ts" setup>
import { ref, defineComponent, defineProps, onMounted, reactive } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import * as echarts from 'echarts';
import useStore from '../store'
import path from 'path'
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import '../StreamPlayTech';
import { send } from 'process';
import { onBeforeRouteLeave } from 'vue-router';
const props = defineProps(['exp_id'])
let ipcRenderer = require('electron').ipcRenderer;

var chartData = [];
var dataCount = 10;
var startTime = 0
let util = require('util')
var types = [
    { name: '理毛', color: '#7b9ce1' },
    { name: '扶墙站立', color: '#bd6d6c' },
    { name: '不扶墙站立', color: '#75d874' },
    { name: '洗脸', color: '#e0bc78'}
    // { name: 'Listeners', color: '#e0bc78' },
    // { name: 'GPU Memory', color: '#dc77dc' },
    // { name: 'GPU', color: '#72b362' }
];

const { experiments } = useStore()
const current_exp = experiments.get_from_id(props.exp_id)
let categories = current_exp.detection_behavior_kinds;
let fs = require("fs")
const displayChart = ref(true)
let array: any = [];
let playerTop: videojs.Player | null = null
let playerSide: videojs.Player | null = null
function getWindowSize() {
    const { offsetWidth, offsetHeight } = document.documentElement
    const { innerHeight } = window // innerHeight will be blank in Windows system
    return [
        offsetWidth,
        innerHeight > offsetHeight ? offsetHeight : innerHeight
    ]
}

try {
    let csv_path = path.join(current_exp.folder_path, 'detection_result.csv')
    let csvstr: string = fs.readFileSync(csv_path, "utf8", 'r+');
    let arr: string[] = csvstr.split('\r\n');
    arr.forEach(line => {
        if (line != '') array.push(line.split(','));
    })
} catch {
    console.log("didn't display chart")
    displayChart.value = false
}
console.log(array)
array.forEach(function (item, index) {
    var typeItem = types[item[0]];
    chartData.push({
        name: typeItem.name,
        value: [Number(item[0]), Number(item[1]), Number(item[2]), Number(item[2] - item[1])],
        itemStyle: {
            normal: {
                color: typeItem.color
            }
        }
    });
})
const run_analysis = () => {
    fetch('http://127.0.0.1:5001/api/wash_recognition', {
        method: 'post',
        body: JSON.stringify({ video_filename: current_exp.folder_path }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (data) {

    })
}

function renderItem(params, api) {
    var categoryIndex = api.value(0);
    var start = api.coord([api.value(1), categoryIndex]);
    var end = api.coord([api.value(2), categoryIndex]);
    var height = api.size([0, 1])[1] * 0.6;
    var rectShape = echarts.graphic.clipRectByRect(
        {
            x: start[0],
            y: start[1] - height / 2,
            width: end[0] - start[0],
            height: height
        },
        {
            x: params.coordSys.x,
            y: params.coordSys.y,
            width: params.coordSys.width,
            height: params.coordSys.height
        }
    );
    return (
        rectShape && {
            type: 'rect',
            transition: ['shape'],
            shape: rectShape,
            style: api.style()
        }
    );
};
function embyPot() {
    let resultvideopath = current_exp.folder_path + "/detection_result.mp4";
    console.log(resultvideopath);
    let poturl = `potplayer://${resultvideopath}`;
    poturl = poturl.replace("\\", "");
    console.log(poturl);
    window.open(poturl, "_parent");
};


const option = ref({
    tooltip: {
        formatter: function (params) {
            return params.marker + params.name + ': ' + params.value[3] + ' ms';
        }
    },
    title: {
        text: '行为图谱',
        left: 'center'
    },
    dataZoom: [
        {
            type: 'slider',
            filterMode: 'weakFilter',
            showDataShadow: false,
            top: 400,
            labelFormatter: '',
            startValue: 0,
            endValue: 100
        },
        {
            type: 'inside',
            filterMode: 'weakFilter'
        }
    ],
    grid: {
        height: 300
    },
    series: [
        {
            type: 'custom',
            renderItem: renderItem,
            itemStyle: {
                opacity: 0.8
            },
            encode: {
                x: [1, 2],
                y: 0
            },
            data: chartData
        },
    ],
    xAxis: {
        min: startTime,
        scale: true,
        axisLabel: {
            formatter: function (val) {
                return Math.max(0, val - startTime) + ' s';
            }
        }
    },
    yAxis: {
        data: categories
    },
})
const videoPlayerTop = ref()
// const videoPlayerSide = ref()
const videoOptionsTop = reactive({
    autoplay: false,
    controls: false,
    width: 800,
    height: 400,
    preload: 'metadata',
    sources: [
        {
            src: 'http://127.0.0.1:8888',
            type: 'video/mp4'
        }
    ],
    techOrder: ['StreamPlay'],
    StreamPlay: { duration: 0 }
})

onMounted(() => {
    ipcRenderer.send('playVideoFromFile', path.join(current_exp.folder_path, 'video.mkv'), path.join(current_exp.folder_path, 'video1.mkv'));
    ipcRenderer.on('videoServerReady', (event, message) => {
        console.log(message, "message")
        let videoOptionsTop = {
            width: 800,
            height: 400,
            autoplay: true,
            controls: true,
            preload: 'metadata',
            sources: [
                {
                    src: 'http://127.0.0.1:8888?startTime=0',
                    type: 'video/mp4'
                }
            ],
            techOrder: ['StreamPlay'],
            StreamPlay: { duration: message.duration }
        }
        console.log(videoPlayerTop)
        playerTop = videojs(videoPlayerTop.value, videoOptionsTop, () => {
            playerTop.log('onPlayerReady', this);
        });
        console.log('videoServerReady-render:', message)
        playerTop.load()
        playerTop.play()
        // playerSide.load()
        // playerSide.play()
    });

    // playerSide = videojs(videoPlayerSide, videoOptionsSide, () => {
    //     playerSide.log('onPlayerReady', this);
    // });

})
onBeforeRouteLeave(() => {
    if (playerTop) {
        playerTop.dispose();
    }
    if (playerSide) {
        playerSide.dispose();
    }
    ipcRenderer.send("stopVideoDisplay")
})
const playVideo = () => {
    playerTop.load()
    playerTop.play()
}
</script>
<style>
.chart {
    width: 80%;
    margin-left: 50px;
}
</style>