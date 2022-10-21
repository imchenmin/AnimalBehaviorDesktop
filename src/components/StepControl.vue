<template>
    <el-steps :active="active" finish-status="success" align-center>
        <el-step title="项目设置" :icon="Edit" @click.native="stepClick(0)" :description="state_msg[0]"/>
        <el-step title="录制" @click.native="stepClick(1)" ref="record_step" :description="state_msg[1]"/>
        <el-step title="分析" @click.native="stepClick(2)" :description="state_msg[2]"/>
    </el-steps>
</template>
<script lang="ts" setup>
import { computed, ref } from 'vue'
import { Edit, Picture, Upload } from '@element-plus/icons-vue'
import useStore from '../store'
import { useRouter } from 'vue-router'

const props = defineProps({
    _id: String,
    active: Number
})
const { experiments } = useStore()

const current_exp = computed(() => experiments.get_from_id(props._id))
const state_msg = computed(() => {
    let arr = new Array()
    let tmp = experiments.get_from_id(props._id)
    console.log(tmp, props._id);
    
    arr[0] = "已完成"
    arr[1] = tmp.record_state? "已录制" : "请录制"
    arr[2] = tmp.record_state? "未分析" : "请录制后分析"
    return arr
})
const router = useRouter()
const stepClick = (item) => {
    if (item == 2 ){
            if (!current_exp.value.record_state) {
                alert("请先录制视频")
                return 
            }else {
                // 判断哪种类型的界面
                let router_prefix = ""
                if (current_exp.value.analysis_method == "tracking") router_prefix = "/arena-settings/"
                if (current_exp.value.analysis_method == "detection") router_prefix = "/detection-result/"
                router.push(router_prefix + current_exp.value._id)
            }
    }
    if (item == 1 && !current_exp.value.record_state) {
        router.push("/camera/" + current_exp.value._id)
    }
    if (item == 0) {
        router.push("/project/" + current_exp.value._id)
    }
}
</script>
<style>
.el-steps{
    margin-top: 20px;
}
</style>