<template lang="">
<el-popover
    placement="bottom"
    title="处理进度"
    :width="400"
    trigger="click">
    <template #reference>
        <el-button size="large"><el-icon><Bell /></el-icon></el-button>
    </template>
    <div>
        <el-button @click="sentHello">查询进度条</el-button>
    </div>
    <div  v-for="project in ProgressList">
        <el-progress
            :percentage="project.progress"
            :text-inside="true"
            :stroke-width="15">
            <span>{{project.project_path}}</span>
        </el-progress>
    </div>

</el-popover>
</template>
<script lang="ts">
import useStore from '../store/index'
import { mapState } from 'pinia'
import { ProcessingObject } from '../objects/ProcessingObject'
import { ElNotification } from 'element-plus'

export default {
    setup(){
        const {experiments} = useStore()
        return {experiments}
    },
    data: () => ({
        messageLis: [],
        ProgressList: new Array<ProcessingObject>()
    }),
    computed: {

    },
    mounted() {
        this.sockets.subscribe('project_status', (data) => {
            // 判断是否存在
            let recvList = data.msg
            console.log(recvList);
            
            if (!recvList) return
            recvList.forEach((po: ProcessingObject) => {
                let firstmatch_idx = this.ProgressList.findIndex((obj) => {
                    return obj.project_path == po.project_path
                })
                if (firstmatch_idx >= 0) {
                    this.ProgressList[firstmatch_idx].progress = po.progress
                } else {
                    this.ProgressList.push(po)
                }
                // if (po.progress >=100) {
                    // // 消息通知
                    // ElNotification({
                    //     title: 'Success',
                    //     message: `项目分析完成 ${po.project_path}`,
                    //     type: 'success',
                    //     duration: 0
                    // })
                // }
            })
        })
    },
    methods: {
        sentHello() {
            this.$socket.emit('require_project_status', {
                project_list: this.experiments.config.openedProjectList
            })
        },
    }
}
</script>
<style>
.el-progress {
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>