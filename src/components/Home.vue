<template lang="">
  <el-card type="border-card" class="intro-panel">
    <template #header>
      <div class="card-header">
        <span>{{ store.softwareName }}</span>
        <el-button class="button" text>Operation button</el-button>
      </div>
    </template>
    <h2>打开实验</h2>
    <h2>新建实验</h2>
    <h2>恢复实验备份</h2>
    <h2>了解更多</h2>
    <h2>新闻</h2>
  </el-card>
</template>
<script>
import { useStore } from '~/stores/store'
export default {
    setup() {
        const store = useStore();
        return {
            store
        }
    }
}
</script>
<style>
.intro-panel {
    width: 600px;
    margin: auto;
    margin-top: 50px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>