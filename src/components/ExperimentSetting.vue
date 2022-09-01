<template>
    <el-scrollbar>
        <el-form :model="form" label-width="120px">
            <h2>实验信息</h2>
            <el-form-item label="实验名称">
                <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="实验类型">
                <el-select v-model="form.region" placeholder="please select your zone">
                    <el-option label="追踪" value="shanghai" />
                    <el-option label="识别" value="beijing" />
                </el-select>
            </el-form-item>
            <el-form-item label="备注">
                <el-input v-model="form.desc" type="textarea" />
            </el-form-item>
            <h2>视频源</h2>
            <el-form-item label="Resources">
                <el-radio-group v-model="form.resource">
                    <el-radio label="视频文件" />
                    <el-radio label="视频流" />
                </el-radio-group>
            </el-form-item>
            <h2>分析选项</h2>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Create</el-button>
                <el-button>Cancel</el-button>
            </el-form-item>
        </el-form>




    </el-scrollbar>

</template>
<script setup>
import { reactive } from 'vue'

// do not use same name with ref
const form = reactive({
    name: '',
    region: '',
    date1: '',
    date2: '',
    delivery: false,
    type: [],
    resource: '',
    desc: '',
})

const onSubmit = () => {
    console.log('submit!')
}
</script>
<style>
</style>