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
    <v-chart v-if="displayChart" class="chart" :option="option" />
    <p v-if="!displayChart">没有结果文件，请确认</p>
    测试
</template>
<script lang="ts" setup>
import { ref, defineComponent, defineProps } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import * as echarts from 'echarts';
import useStore from '../store'
import path from 'path'

const props = defineProps(['exp_id'])
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
// Generate mock data
const { experiments } = useStore()
const current_exp = experiments.get_from_id(props.exp_id)
let categories = current_exp.detection_behavior_kinds;
let fs = require("fs")
const displayChart = ref(true)
let array: any = [];

try {
    let csv_path = path.join(current_exp.folder_path, 'detection_result.csv')
    let csvstr: string = fs.readFileSync(csv_path, "utf8", 'r+');
    let arr: string[] = csvstr.split('\r\n');
    arr.forEach(line => {
        if (line !='')         array.push(line.split(','));
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
        value: [Number(item[0]), Number(item[1]), Number(item[2]), Number(item[2]-item[1])],
        itemStyle: {
            normal: {
                color: typeItem.color
            }
        }
    });
})
console.log(chartData)
function renderItem(params, api) {
    console.log(api.value,params)
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
            labelFormatter: ''
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
</script>
<style>

</style>