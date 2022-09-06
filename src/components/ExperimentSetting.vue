<template>
    <el-scrollbar>
        <el-dialog v-model="createNewProjectVisible" title="新建项目">
            <el-form ref="ruleFormRef" :model="form" :rules="rules" label-width="120px">
                <h2>实验信息</h2>
                <el-form-item label="实验名称" prop="name">
                    <el-input v-model="form.name" />
                </el-form-item>
                <el-form-item label="实验类型" prop="type">
                    <el-select v-model="form.type" placeholder="please select your zone">
                        <el-option label="追踪" value="tracking" />
                        <el-option label="识别" value="detection" />
                    </el-select>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="form.desc" type="textarea" />
                </el-form-item>
                <el-form-item label="日期" prop="date1">
                    <el-date-picker v-model="form.date1" type="date" placeholder="Pick a date" />
                </el-form-item>
                <el-form-item label="项目路径">
                    <el-button @click="onSelectFolder">选择文件夹</el-button>
                    <p> {{ folder_path }}</p>
                </el-form-item>
                <el-form-item label="输入小鼠信息">
                    <el-switch v-model="form.record_mouse_info" />
                </el-form-item>
                <div class="detection-setting" v-if="form.record_mouse_info">
                    <h2>小鼠信息</h2>
                    <el-form-item label="小鼠性别">
                        <el-select v-model="form.mouse_gender" placeholder="性别">
                            <el-option label="雄性" value="male" default />
                            <el-option label="雌性" value="female" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="小鼠出生日期">
                        <el-date-picker v-model="form.mouse_dob" type="date" placeholder="Pick a day" />
                    </el-form-item>
                    <el-form-item label="小鼠基因型">
                        <el-input v-model="form.mouse_genetype" />
                    </el-form-item>

                </div>
                <div class="detection-setting" v-if="form.type == 'detection'">
                    <h2>精细行为分析选项</h2>
                    <el-form-item label="小鼠数量" prop="tracking_mouse_number">
                        <el-select v-model="form.tracking_mouse_number" placeholder="数量">
                            <el-option label="1" value=1 />
                            <el-option label="2" value=2 />
                        </el-select>
                    </el-form-item>
                </div>
                <div class="tracking-setting" v-if="form.type == 'tracking'">
                    <h2>追踪分析选项</h2>
                </div>
                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRef)" :disabled="!isReadyToCreate">Create
                    </el-button>
                    <el-button>Cancel</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
        <el-header>
            <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/' }">Projects</el-breadcrumb-item>
            </el-breadcrumb>
        </el-header>
        <el-button @click="createNewProjectVisible = true">添加新项目</el-button>
        <el-table :data="tabledata">
            <el-table-column prop="name" label="项目名" />
            <el-table-column prop="analysis_method" label="项目类型" />
            <el-table-column label="拍摄状态">
                <template #default="scope">
                    <div v-if="!scope.row.record_state">文件未录制，请
                        <router-link :to="{ path: '/camera/' + scope.row._id }">录制</router-link>
                    </div>
                    <div v-if="scope.row.record_state">已录制</div>
                </template>
            </el-table-column>
            <el-table-column label="查看结果">
                <template #default="scope">
                    <div v-if="!scope.row.record_state">-</div>
                    <div v-if="scope.row.record_state">
                        <div v-if="scope.row.analysis_method == 'tracking'">
                            <router-link :to="{ path: '/arena-settings/' + scope.row._id }">查看</router-link>
                        </div>
                        <router-link :to="{ path: '/detection-result/' + scope.row._id }"
                                v-if="scope.row.analysis_method == 'detection'">处理</router-link>
                        <div v-if="scope.row.detection_state">
                            <router-link :to="{ path: '/detection-result/' + scope.row._id }">查看</router-link>
                        </div>
                    </div>

                </template>
            </el-table-column>

        </el-table>
    </el-scrollbar>

</template>
<script setup lang="ts">
import { reactive } from 'vue'
import { computed, ref, onBeforeMount, nextTick } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import useStore from '../store'
import path from 'path'
import ExperiemntObj from '../objects/experiment'
import { lte } from 'lodash'


const { settings, experiments, } = useStore()
const tabledata = experiments.opened_project
let fs = require("fs")
let util = require('util')
const ruleFormRef = ref<FormInstance>()
const createNewProjectVisible = ref(false)
experiments.loadProject()
const isVideoExist = async (row) => {
    let current_project = experiments.get_from_id(row._id)
    if (!current_project) return false
    const exists = await util.promisify(fs.exists)(path.join(current_project.folder_path, 'video.mp4'))
    console.log(exists)
    return exists

}
const isResultExist = (_id: string) => {
    return false
}
const form = reactive({
    name: '',
    date1: new Date(),
    type: '',
    desc: '',
    parent_path: '',
    record_mouse_info: false,
    mouse_gender: '',
    mouse_genetype: '',
    mouse_dob: new Date(),
    tracking_mouse_number: 1
})

settings.getHomeDir()
form.parent_path = settings.default_parent_folder
const checkFolderExist = (rule: any, value: any, callback: any) => {
    if (!value) {
        return callback(new Error('Please input the age'))
    }
    fs.exists(folder_path.value, function (exists) {
        if (exists) {
            return callback(new Error('已存在项目，请重命名'))
        } else {
            return callback()
        }
    })
}

const rules = reactive<FormRules>({
    name: [
        { required: true, message: '请输入实验名', trigger: 'change' },
        { min: 3, max: 20, message: '长度至少为3，不超过30', trigger: 'change' },
        { validator: checkFolderExist, trigger: 'change' }
    ],
    type: [
        { required: true, message: '请选择实验类型', trigger: 'change' }
    ],
    date1: [
        { required: true, message: '请选择日期', trigger: 'change' }
    ],
    tracking_mouse_number: [
        { required: true, message: '请输入小鼠数量', trigger: 'change' },
    ]

})

const folder_path = computed(() => form.parent_path + '/' + form.name)
const isReadyToCreate = computed(() => form.name != '' && form.parent_path != '' && form.type != '')
const onSelectFolder = () => {
    const { dialog } = require('@electron/remote')
    dialog.showOpenDialog({
        title: '保存图像文件',
        defaultPath: '/',
        properties: ['openDirectory']
    }).then((val) => {
        form.parent_path = val.filePaths[0]
    })
}
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('submit!')
            // TODO: 新建文件夹
            fs.exists(folder_path.value, function (exists) {
                if (exists) {
                    console.log('folder exist!')
                } else {
                    fs.mkdir(folder_path.value, function (error) {
                        console.log(error)
                        if (!error) {
                            let record = {
                                folder_path: folder_path.value,
                                name: form.name,
                                description: form.desc,
                                analysis_method: form.type,
                                date: form.date1,
                                record_mouse_info: form.record_mouse_info,
                                mouse_gender: form.mouse_gender,
                                mouse_genetype: form.mouse_genetype,
                                mouse_dob: form.mouse_dob,
                                tracking_mouse_number: form.tracking_mouse_number,
                                detection_behavior_kinds: ['a'],
                                record_state: false,
                                detection_state: false,
                                tracking_state: false

                            } as ExperiemntObj
                            let ret = experiments.addProject(record)
                            tabledata.push(record)
                            createNewProjectVisible.value = false
                            formEl.resetFields()
                        }
                    })
                }
            })
        } else {
            console.log('error submit!', fields)
        }
    })
}

</script>
<style>
h2 {
    padding-left: 60px;
}
</style>