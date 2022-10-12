<template lang="">
    <el-dialog v-model="settings.showSettingWidgt" class="setting-dialog">
        <h2>软件设置</h2>
        <el-tabs :tab-position="tabPosition" style="height: 200px" class="demo-tabs">
            <el-tab-pane label="一般设置">
                <p>默认存放地址</p>

            </el-tab-pane>
            <el-tab-pane label="相机设置">
                <el-button @click="getCameraList">加载相机</el-button>
        <div v-if="experiments">
            <div v-for="device in experiments.config.cameraList">
            <el-checkbox  v-model="device.select" @change="updateConfigWrapper">
                {{device.name}}
            </el-checkbox>
            <textarea>{{device.alternativeName}}</textarea>
            </div>

        </div>
            </el-tab-pane>
            <el-tab-pane label="关于">Task</el-tab-pane>
        </el-tabs>

    </el-dialog>

</template>
<script lang="ts" setup>
//获取setting db
//获取ffmpeg列表
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import useStore from '../store'
import CameraObject from '../objects/CameraObject'

const { settings,experiments } = useStore()
const config = experiments.config
console.log(config);

//强制重新加载
const getCameraList = async () => {
    //调用camera list
    const { parse } = require('ffmpeg-device-list-parser');
    experiments.config.cameraList = new Array<CameraObject>();
    await parse((result) => {
        console.log(result);
        let devicelist = result.videoDevices.filter(p => p.alternativeName.includes("usb#vid"))
        devicelist.forEach(element => {
            let curCam = new CameraObject()
            curCam.name = element.name;
            curCam.alternativeName = element.alternativeName;
            curCam.selected = false;
            experiments.config.cameraList.push(curCam)
        });
    });
}
const updateConfigWrapper = () => {
    experiments.updateConfig()
}
</script>
<style lang="">
    
</style>