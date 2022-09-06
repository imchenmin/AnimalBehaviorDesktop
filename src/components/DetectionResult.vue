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
    <v-chart class="chart" :option="option" />
    <p> as</p>
</template>
<script lang="ts">
import { ref, defineComponent } from 'vue';
import VChart, { THEME_KEY } from 'vue-echarts';
import * as echarts from 'echarts';
import useStore from '../store'

export default defineComponent({
    props: {
        exp_id: String
    },
    setup(props) {
        var data = [];
        var dataCount = 10;
        var startTime = +new Date();
        var categories = ['categoryA', 'categoryB', 'categoryC'];
        var types = [
            { name: 'JS Heap', color: '#7b9ce1' },
            { name: 'Documents', color: '#bd6d6c' },
            { name: 'Nodes', color: '#75d874' },
            { name: 'Listeners', color: '#e0bc78' },
            { name: 'GPU Memory', color: '#dc77dc' },
            { name: 'GPU', color: '#72b362' }
        ];
        // Generate mock data
        const { experiments } = useStore()

        categories.forEach(function (category, index) {
            var baseTime = startTime;
            for (var i = 0; i < dataCount; i++) {
                var typeItem = types[Math.round(Math.random() * (types.length - 1))];
                var duration = Math.round(Math.random() * 10000);
                data.push({
                    name: typeItem.name,
                    value: [index, baseTime, (baseTime += duration), duration],
                    itemStyle: {
                        normal: {
                            color: typeItem.color
                        }
                    }
                });
                baseTime += Math.round(Math.random() * 2000);
            }
        })
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
        const option = ref({
            tooltip: {
                formatter: function (params) {
                    return params.marker + params.name + ': ' + params.value[3] + ' ms';
                }
            },
            title: {
                text: 'Profile',
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
                    data: data
                },
            ],
            xAxis: {
                min: startTime,
                scale: true,
                axisLabel: {
                    formatter: function (val) {
                        return Math.max(0, val - startTime) + ' ms';
                    }
                }
            },
            yAxis: {
                data: categories
            },
        });
        const current_exp = experiments.get_from_id(props.exp_id)

        return { option,current_exp };
    },
});
</script>
<style lang="">
    
</style>