<template >
    编辑和存放实验组结构的地方。比如每一只动物对应的视频和组别。实验组，控制组。
    <el-form :model="record">
        <el-form-item label="实验名">
            <el-input v-model="record.name" />
        </el-form-item>
        <el-form-item>
                <el-button type="primary" @click="handleAdd">Create</el-button>
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
        }
    },
}
</script>
<style lang="">
    
</style>