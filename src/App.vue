<template>
  <el-container class="common-layout">
    <el-aside>
      <project-side-bar></project-side-bar>
    </el-aside>
    <el-container>
      <el-main class="main">
        <router-view :key="$route.fullPath"></router-view>
      </el-main>
    </el-container>
  </el-container>
  <SoftwareSettings></SoftwareSettings>

</template>

<script lang="ts" setup>
import ProjectSideBar from './components/ProjectSideBar.vue';

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

.common-layout .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}

.common-layout .el-menu {
  border-right: none;
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