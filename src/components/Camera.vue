<template >
    <el-header>
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
    </el-header>


    <el-form :model="record">
        <el-form-item>
            <el-button type="primary" @click="handleOpen" v-if="cameraflag">打开相机</el-button>
            <el-button type="primary" @click="handleClose" v-else>关闭相机</el-button>
            <el-button type="primary" @click="handleStart" v-if="!cameraflag && recordflag">开始录制</el-button>
            <el-button type="primary" @click="handleStop" v-if="!cameraflag && ! recordflag">关闭录制</el-button>
        </el-form-item>
    </el-form>

</template>
<script lang="ts">
import useStore from '../store'
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
        recordflag: true
    }),
    computed: {
        current_exp() {
            const { experiments } = useStore()
            // console.log(this.exp_id,this.$router.params.exp_id)
            return experiments.get_from_id(this.exp_id)
        }
    },
    methods: {
        handleOpen() {
                fetch('http://127.0.0.1:5001/api/open_camera', {
                method: 'post',
                body: JSON.stringify({ a: 1 }),
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
                body: JSON.stringify({ video_filename: this.current_exp.folder_path }),
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
                body: JSON.stringify({ video_filename: this.current_exp.folder_path }),
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