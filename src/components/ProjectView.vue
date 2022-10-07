<template>

    <step-control :_id="_id" :active="0"></step-control>
    <!-- <router-link :to="'/camera/'+_id">录制</router-link>
    <router-link :to="'/arena-settings/'+_id">追踪结果</router-link>
    <router-link :to="'/detection-result/'+_id">行为识别结果</router-link> -->
    <el-form ref="ruleFormRef" :model="current_exp" label-width="120px" size="large">
        <h2>项目信息</h2>
        <el-form-item label="实验名称" prop="name">
            <el-input v-model="current_exp.name" disabled />
        </el-form-item>
        <el-form-item label="实验类型" prop="type">
            <el-select v-model="current_exp.analysis_method" placeholder="please select your zone" disabled>
                <el-option label="追踪" value="tracking" />
                <el-option label="识别" value="detection" />
            </el-select>
        </el-form-item>
        <el-form-item label="备注">
            <el-input v-model="current_exp.description" type="textarea" />
        </el-form-item>
        <!-- <el-form-item label="日期" prop="date">
            <el-date-picker v-model="current_exp.date" type="date" placeholder="Pick a date" />
        </el-form-item> -->
        <el-form-item label="项目路径">
            <p class="form-custom-item"> {{ current_exp.folder_path }}</p>
        </el-form-item>

        <h2>小鼠信息</h2>
        <el-form-item label="小鼠性别">
            <el-select v-model="current_exp.mouse_gender" placeholder="性别">
                <el-option label="雄性" value="male" default />
                <el-option label="雌性" value="female" />
            </el-select>
        </el-form-item>
        <el-form-item label="小鼠出生日期">
            <el-date-picker v-model="current_exp.mouse_dob" type="date" placeholder="Pick a day" />
        </el-form-item>
        <el-form-item label="小鼠基因型">
            <el-input v-model="current_exp.mouse_genetype" />
        </el-form-item>

        <div class="detection-setting" v-if="current_exp.analysis_method == 'detection'">
            <h2>精细行为分析选项</h2>
            <el-form-item label="小鼠数量" prop="tracking_mouse_number">
                <el-select v-model="current_exp.tracking_mouse_number" placeholder="数量">
                    <el-option label="1" value=1 />
                    <el-option label="2" value=2 />
                </el-select>
            </el-form-item>
        </div>
        <div class="tracking-setting" v-if="current_exp.analysis_method == 'tracking'">
            <h2>追踪分析选项</h2>
        </div>
        <el-form-item>
            <el-button type="primary" @click="updateForm(ruleFormRef)">修改
            </el-button>
            <el-button>取消修改</el-button>
            <el-button @click="closeProjectWrapper">关闭项目</el-button>
        </el-form-item>
    </el-form>

</template>
<script lang="ts" setup>
import { Edit, Picture, SuccessFilled, Upload } from '@element-plus/icons-vue'
import useStore from '../store'
import { computed, ref,reactive } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'

const ruleFormRef = ref<FormInstance>()
const record_step = ref()
const active = ref(0)
const props = defineProps({
    _id: String
})
const { experiments } = useStore()
console.log(props)
const current_exp = experiments.get_from_id(props._id)
const state_msg = computed(() => {
    let arr = new Array()
    arr[0] = "已完成"
    arr[1] = current_exp.value.record_state ? "已录制" : "请录制"
    arr[2] = current_exp.value.record_state ? "未分析" : "请录制后分析"
    return arr
})
const router = useRouter()
const stepClick = (item) => {
    if (item != '' || item != null) {
        if (item == 2) {
            if (!current_exp.value.record_state) {
                alert("请先录制视频")
                return
            } else {
                // 判断哪种类型的界面
                let router_prefix = ""
                if (current_exp.value.analysis_method == "tracking") router_prefix = "/arena-settings/"
                if (current_exp.value.analysis_method == "detection") router_prefix = "/detection-result/"
                router.push(router_prefix + current_exp.value._id)
            }
        }
        // active.value = item 
    }
    if (item == 1 && !current_exp.value.record_state) {
        router.push("/camera/" + current_exp.value._id)
    }
}
const rules = reactive<FormRules>({
    name: [
        { required: true, message: '请输入实验名', trigger: 'change' },
        { min: 3, max: 20, message: '长度至少为3，不超过30', trigger: 'change' }
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
const updateForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('update')
            experiments.updateProject(current_exp).then(() => {
                console.log("updated")
            })
            formEl.resetFields()
        } else {
            console.log('error submit!', fields)
        }
    })
}
const closeProjectWrapper = () => {
    experiments.closeProject(current_exp._id)
}
</script>
<style scoped>
.form-custom-item {
    height: 40px;
    line-height: 40px;
    margin: 0;
}
</style>