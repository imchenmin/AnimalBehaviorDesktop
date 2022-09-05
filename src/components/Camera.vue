<template >
    <p>    编辑和存放实验组结构的地方。比如每一只动物对应的视频和组别。实验组，控制组。</p>
    <el-form :model="record">
        <el-form-item label="实验名">
            <el-input v-model="record.name" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="handleOpen">打开相机</el-button>
            <el-button type="primary" @click="handleStart">开始录制</el-button>
            <el-button type="primary" @click="handleStop">结束录制</el-button>
            <el-button type="primary" @click="handleClose">关闭相机</el-button>
            <el-button>Cancel</el-button>
        </el-form-item>
    </el-form>

</template>
<script lang="ts">
import useStore from '../store'

export default {
    data: () => ({
        record: {
            name: '',
            sex: 0,
            video_path: '',
            note: '',
            genotype: '',
            datetime: ''
        }
    }),
    methods: {
        handleAdd() {
            const { experiments } = useStore()
            experiments.addRecord(this.record)
            this.$router.push('/')
            
        },
        handleOpen(){
            fetch('http://127.0.0.1:5001/api/open_camera', {
                method: 'post',
                body: JSON.stringify({a:1}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(data) {
            })
        },
        handleStart(){
            fetch('http://127.0.0.1:5001/api/start_record', {
                method: 'post',
                body: JSON.stringify({a:1}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(data) {
            })
        },
        handleStop(){
            fetch('http://127.0.0.1:5001/api/stop_record', {
                method: 'post',
                body: JSON.stringify({a:1}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(data) {
            })
        },
        handleClose(){
            fetch('http://127.0.0.1:5001/api/close_camera', {
                method: 'post',
                body: JSON.stringify({a:1}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(data) {
            })
        }
    },
}
</script>
<style lang="">
    
</style>