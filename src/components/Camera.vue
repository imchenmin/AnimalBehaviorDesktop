<template >
    <step-control :_id="current_exp._id" :active="1"></step-control>
    <el-button type="primary" @click="run_preview" v-if="cameraflag">打开相机</el-button>
    <el-button type="primary" @click="stop_preview" v-else>关闭相机</el-button>
    <el-button type="primary" @click="handleStart" v-if="!cameraflag && recordflag">开始录制</el-button>
    <el-button type="primary" @click="handleStop" v-if="!cameraflag && ! recordflag">关闭录制</el-button>
    <div v-show="!cameraflag">
        <!-- 默认考虑4个摄像头的布局 -->

        <!-- <div v-for="(camera,index) in cameraList">

            <p>{{camera.name}}</p>
            <video :ref="setVideoRef" :key="camera.alternativeName" muted autoplay></video>
        </div> -->
        <el-row>
            <el-col :span="8" v-if="cameraList[0]">
                <p>{{cameraList[0].name}}</p>
                <video :ref="setVideoRef" :key="cameraList[0].alternativeName" muted autoplay></video>
            </el-col>
            <el-col :span="8" v-if="cameraList[1]">
                <p>{{cameraList[1].name}}</p>
                <video :ref="setVideoRef" :key="cameraList[1].alternativeName" muted autoplay></video>
            </el-col>
            <el-col :span="8" v-if="cameraList[2]">
                <p>{{cameraList[2].name}}</p>
                <video :ref="setVideoRef" :key="cameraList[2].alternativeName" muted autoplay></video>
            </el-col>
            <el-col :span="8" v-if="cameraList[3]">
                <p>{{cameraList[3].name}}</p>
                <video :ref="setVideoRef" :key="cameraList[3].alternativeName" muted autoplay></video>
            </el-col>
        </el-row>
    </div>


</template>
<script lang="ts">
import useStore from '../store'
let ipcRenderer = require('electron').ipcRenderer;

import flvjs from "flv.js";
import path from 'path'
import CameraObject from '../objects/CameraObject';
export default {
    props: ['exp_id'],
    data: () => ({
        video_name: 'video.mp4',
        video_path: '',
        note: '',
        genotype: '',
        datetime: '',
        current_exp_id: '',
        cameraflag: true,
        recordflag: true,
        players: [],
        cameraList: [],
        itemRefs: [],
    }),
    computed: {
        current_exp() {
            const { experiments } = useStore()
            // console.log(this.exp_id,this.$router.params.exp_id)
            return experiments.get_from_id(this.exp_id)
        }
    },
    beforeMount() {
        const { experiments } = useStore()
        this.cameraList = experiments.getActiveRTSPList()
    },
    mounted() {
        console.log(this.itemRefs)
        if (flvjs.isSupported()) {
            this.itemRefs.forEach((element, index) => {
                let vidoeitem = flvjs.createPlayer({
                    type: "flv",
                    isLive: true,
                    url: `ws://localhost:8899/rtsp/${index}/?url=${this.cameraList[index].alternativeName}`
                });
                console.log(vidoeitem)
                vidoeitem.attachMediaElement(element);

                try {
                    vidoeitem.load();
                    vidoeitem.play();
                } catch (error) {
                    console.log(error);
                };
                this.players.push(vidoeitem)
            });
        }
    },
    beforeUnmount() {
        // if (this.playerTop) {
        //     this.playerTop.dispose();
        // }
        // if (this.playerSide) {
        //     this.playerSide.dispose();
        // }
    },
    beforeRouteLeave(to, from) {
        console.log("router leave")
        ipcRenderer.send("stopRecord")
    },
    methods: {
        setVideoRef(el) {
            this.itemRefs.push(el)
        },
        run_preview() {
            ipcRenderer.send("ipcRendererReady", "true");
            ipcRenderer.send('cameraRecording', this.current_exp.folder_path, JSON.stringify(this.cameraList));
            ipcRenderer.on('cameraRecoridngReady', (event, message) => {
                console.log('cameraRecoridng-render:', message)
                setTimeout(() => {
                    this.players.forEach(element => {
                        element.load();
                        element.play();
                    }, 5000);
                })

            });
            this.cameraflag = false
        },
        stop_preview() {
            this.current_exp.record_state = true; // 需要考虑没有成功录制的情况，暂存
            console.log(this.current_exp);
            ipcRenderer.send("stopRecord")
            this.cameraflag = true
        },
        handleOpen() {
            fetch('http://127.0.0.1:5001/api/open_camera', {
                method: 'post',
                body: JSON.stringify({ analyzer: this.current_exp.analysis_method }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function (data) {
            })
            this.cameraflag = false
        },
        handleStart() {
            fetch('http://127.0.0.1:5001/api/start_record', {
                method: 'post',
                body: JSON.stringify({ video_filename: this.current_exp.folder_path, analyzer: this.current_exp.analysis_method }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function (data) {
            })
            this.recordflag = false
        },
        handleStop() {
            fetch('http://127.0.0.1:5001/api/stop_record', {
                method: 'post',
                body: JSON.stringify({ video_filename: this.current_exp.folder_path, analyzer: this.current_exp.analysis_method }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function (data) {
            })
            this.recordflag = true
        },
        handleClose() {
            fetch('http://127.0.0.1:5001/api/close_camera', {
                method: 'post',
                body: JSON.stringify({ video_filename: this.current_exp.folder_path }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function (data) {
            })
            this.cameraflag = true
        }
    },
}
</script>
<style lang="scss">
.el-row {
    margin-bottom: 20px;
}

.el-row:last-child {
    margin-bottom: 0;
}

.el-col {
    border-radius: 4px;
}

.grid-content {
    border-radius: 4px;
    min-height: 200px;
}
</style>