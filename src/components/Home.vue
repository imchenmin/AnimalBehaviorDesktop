<template lang="">
  <el-card type="border-card" class="intro-panel">
    <template #header>
      <div class="card-header">
        <span>{{ version.softwareName }}</span>
        <el-button class="button" text>Operation button</el-button>
      </div>
    </template>
    <h2>打开实验</h2>
    <h2>新建实验</h2>
    <h2>恢复实验备份</h2>
    <h2>了解更多</h2>
    <h2>新闻</h2>
  </el-card>
  <div>下面存放处理列表，来保证让用户知道现在在处理什么</div>
</template>
<script>
import useStore from '~/store'
export default {
  setup() {
    const { version } = useStore();
    return {
      version
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