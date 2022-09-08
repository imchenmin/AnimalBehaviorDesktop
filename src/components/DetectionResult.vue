<template lang="">
    <el-page-header @back="$router.push('/')">
        <template #breadcrumb>
            <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/' }">Projects</el-breadcrumb-item>
                <el-breadcrumb-item :to="{ path: '/' }">{{ current_exp.name }}</el-breadcrumb-item>
                <el-breadcrumb-item :to="{ path: '/' }">Camera</el-breadcrumb-item>
            </el-breadcrumb>
        </template>
        <template #content>
            <span> {{ current_exp.name }} </span>
        </template>
    </el-page-header>
    <el-button v-if="displayChart"  value="查看结果" id="showresult" @click="embyPot">查看结果</el-button>
    <el-button  value="查看结果" id="showresult" @click="run_analysis">分析</el-button>
    <div id="video-container"></div>
    <v-chart v-if="displayChart" class="chart" :option="option" />
</template>
<script lang="ts" setup>
import { ref, defineComponent, defineProps, onMounted } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import * as echarts from 'echarts';
import useStore from '../store'
import path from 'path'
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import '../StreamPlayTech';
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
let videoContainer = document.getElementById("video-container")
console.log(videoContainer)
function getWindowSize() {
    const { offsetWidth, offsetHeight } = document.documentElement
    const { innerHeight } = window // innerHeight will be blank in Windows system
    return [
        offsetWidth,
        innerHeight > offsetHeight ? offsetHeight : innerHeight
    ]
}
function createVideoHtml(source) {
    const [width, height] = [800,400]
    const videoHtml =
        `<video id="my-video" class="video-js vjs-big-play-centered" controls preload="auto" width="${width}"
    height="${height}" data-setup="{}">
    <source src="${source}" type="video/mp4">
    <p class="vjs-no-js">
    To view this video please enable JavaScript, and consider upgrading to a web browser that
    <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
    </p>
    </video>`
    return videoHtml;
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
onMounted(() => {
    let player: videojs.Player | null = null
    ipcRenderer.on('fileSelected', function (event, message) {
        console.log('fileSelected:', message)
        let videoContainer = document.getElementById("video-container")
        videoContainer.innerHTML = createVideoHtml(message.videoSource);
        let vid = document.getElementById("my-video");
        if (message.type === 'native') {
            player = videojs(vid);
            player.play();
            console.log(player)

        } else if (message.type === 'stream') {
            player = videojs(vid, {
                techOrder: ['StreamPlay'],
                StreamPlay: { duration: message.duration }
            }, () => {
                player.play()
            });
        }
        // player.textTrackSettings.setDefaults();
        // player.textTrackSettings.setValues(newSettings);
        // player.textTrackSettings.updateDisplay();
        player.on("progress",(event)=>{
            console.log('buffer',player.currentTime())
            option.value.dataZoom[0].startValue = player.currentTime() - 5
            option.value.dataZoom[0].endValue = player.currentTime() + 5
        })

    });
    ipcRenderer.send("ipcRendererReady", "true");
    ipcRenderer.send('fileDrop', path.join(current_exp.folder_path, 'video.mp4'));

})
</script>
<style>

</style>