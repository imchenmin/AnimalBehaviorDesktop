<template>
  <el-container class="common-layout">
    <el-header>
      <h2 class="title" v-if="experiments.current_experiment">项目：{{experiments.current_experiment.name}}</h2>
      <h2 class="title" v-else>启动页</h2>

    </el-header>
    <el-container>
      <el-aside>
        <project-side-bar></project-side-bar>
      </el-aside>
      <el-main class="main">
        <router-view :key="$route.fullPath"></router-view>
      </el-main>
    </el-container>

  </el-container>
  <SoftwareSettings></SoftwareSettings>

</template>

<script setup lang="ts">
import useStore from './store'
const { settings, experiments } = useStore()
</script>
<style scoped>
* {
  -webkit-touch-callout: none;
  /*系统默认菜单被禁用*/
  -webkit-user-select: none;
  /*webkit浏览器*/
  -khtml-user-select: none;
  /*早期浏览器*/
  -moz-user-select: none;
  /*火狐*/
  -ms-user-select: none;
  /*IE10*/
  user-select: none;
}

.common-layout .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
  padding: 0;
}
.el-header .title {
  text-align: center;
}
.common-layout .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
  width: 300px;
}

.common-layout .el-menu {
  border-right: 2px;
}

.common-layout .el-main {
  padding: 0;
}

a {
  text-decoration-line: none;
}

.common-layout {
  height: 100%;
}

body {
  margin: 0;
  padding: 0;
}

.main {
  margin-left: 20px;
  margin-right: 20px;
}
</style>