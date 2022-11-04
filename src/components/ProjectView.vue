<template>

    <step-control :_id="_id" :active="0"></step-control>
    <!-- <router-link :to="'/camera/'+_id">录制</router-link>
    <router-link :to="'/arena-settings/'+_id">追踪结果</router-link>
    <router-link :to="'/detection-result/'+_id">行为识别结果</router-link> -->
    <el-form ref="ruleFormRef" :model="current_exp" label-width="120px" size="large">


        <el-form-item label="备注">
            <el-input v-model="current_exp.description" type="textarea" />
        </el-form-item>
        <!-- <el-form-item label="日期" prop="date">
            <el-date-picker v-model="current_exp.date" type="date" placeholder="Pick a date" />
        </el-form-item> -->
        <el-form-item label="项目路径">
            <el-button>{{ current_exp.folder_path }}</el-button>
            <span>(点击打开)</span>
        </el-form-item>
        <el-form-item label="标签">
            <el-tag v-for="tag in current_exp.tags" :key="tag" class="mx-1" closable :disable-transitions="false"
                @close="handleClose(tag)">
                {{ tag }}
            </el-tag>
            <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="ml-1 w-20" size="small"
                @keyup.enter="handleInputConfirm" @blur="handleInputConfirm" />
            <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput">
                + New Tag
            </el-button>
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
import { computed, ref, reactive,nextTick } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElInput } from 'element-plus'

const ruleFormRef = ref<FormInstance>()
const record_step = ref()
const active = ref(0)
const inputValue = ref('')
const inputVisible = ref(false)
const InputRef = ref<InstanceType<typeof ElInput>>()

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
const handleClose = (tag: string) => {
    current_exp.tags.splice(current_exp.tags.indexOf(tag), 1)
}
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
                // router_prefix = "/arena-settings/"
                router_prefix = "/detection-result/"
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
const handleInputConfirm = () => {
  if (inputValue.value) {
    current_exp.tags.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}
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
const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value!.input!.focus()
  })
}
</script>
<style scoped>
.form-custom-item {
    height: 40px;
    line-height: 40px;
    margin: 0;
}
</style>