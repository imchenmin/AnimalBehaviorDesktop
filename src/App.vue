<template>
  <el-container class="common-layout">
    <el-container>
      <el-main>
        <el-button><router-link to="/">home</router-link></el-button>
        <el-button><router-link to="/exp-settings">实验设置</router-link></el-button>
        <el-button><router-link to="/camera">拍摄录制</router-link></el-button>
        <el-button><router-link to="/arena-settings">区域分析</router-link></el-button>
        <el-button><router-link to="/detection-result">结果分析</router-link></el-button>
        <router-view></router-view>
      </el-main>
      <el-footer>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
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
</style>