<template >
    <step-control :_id="current_exp._id" :active="1"></step-control>
    <el-form :model="record">
        <el-form-item>
            <el-button type="primary" @click="run_preview" v-if="cameraflag">打开相机</el-button>
            <el-button type="primary" @click="stop_preview" v-else>关闭相机</el-button>
            <el-button type="primary" @click="handleStart" v-if="!cameraflag && recordflag">开始录制</el-button>
            <el-button type="primary" @click="handleStop" v-if="!cameraflag && ! recordflag">关闭录制</el-button>
        </el-form-item>
    </el-form>
    <div v-show="!cameraflag" >
        <video ref="videoPlayerTop" class="video-js"></video>
        <video ref="videoPlayerSide" class="video-js"></video>
    </div>

</template>
<script lang="ts">
import useStore from '../store'
let ipcRenderer = require('electron').ipcRenderer;
import videojs from 'video.js';

import path from 'path'
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
        playerTop: null,
        playerSide: null,
        videoOptionsTop: {
            autoplay: false,
            controls: false,
            width: 800,
            height: 400,
            preload: 'metadata',
            sources: [
                {
                    src: 'http://127.0.0.1:8889',
                    type: 'video/mp4'
                }
            ],
            techOrder: ['StreamPlay']
        },
        videoOptionsSide: {
            autoplay: false,
            controls: false,
            width: 800,
            height: 400,
            preload: 'metadata',
            sources: [
                {
                    src: 'http://127.0.0.1:8890',
                    type: 'video/mp4'
                }
            ],
            techOrder: ['StreamPlay']
        }

    }),
    computed: {
        current_exp() {
            const { experiments } = useStore()
            // console.log(this.exp_id,this.$router.params.exp_id)
            return experiments.get_from_id(this.exp_id)
        }
    },
    mounted() {
        this.playerTop = videojs(this.$refs.videoPlayerTop, this.videoOptionsTop, () => {
            this.playerTop.log('onPlayerReady', this);
        });
        this.playerSide = videojs(this.$refs.videoPlayerSide, this.videoOptionsSide, () => {
            this.playerSide.log('onPlayerReady', this);
        });
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
        if (this.playerTop) {
            this.playerTop.dispose();
        }
        if (this.playerSide) {
            this.playerSide.dispose();
        }
        const { experiments } = useStore()
        // experiments.loadProject()

        ipcRenderer.send("stopRecord")

    },
    methods: {
        run_preview() {
            ipcRenderer.send("ipcRendererReady", "true");
            ipcRenderer.send('cameraRecording', path.join(this.current_exp.folder_path, 'video.mkv'), path.join(this.current_exp.folder_path, 'video1.mkv'));
            ipcRenderer.on('cameraRecoridngReady',  (event, message)=> {
                console.log('cameraRecoridng-render:', message)
                this.playerTop.load()
                this.playerTop.play()
                this.playerSide.load()
                this.playerSide.play()
            });
            this.cameraflag = false
        },
        stop_preview() {
            this.current_exp.record_state=true; // 需要考虑没有成功录制的情况，暂存
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
                body: JSON.stringify({ video_filename: this.current_exp.folder_path, analyzer: this.current_exp.analysis_method}),
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
                body: JSON.stringify({ video_filename: this.current_exp.folder_path , analyzer: this.current_exp.analysis_method}),
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
<style lang="">
    
</style>