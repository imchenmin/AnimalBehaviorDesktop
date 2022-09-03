<template>
  <el-container class="common-layout">
    <el-header style="text-align: right; font-size: 12px">
      <el-menu :default-active="activeIndex2" class="el-menu-demo" mode="horizontal" background-color="#545c64"
        text-color="#fff" active-text-color="#ffd04b" @select="handleSelect">
        <el-menu-item index="1">
          <router-link to="/">Gianttek</router-link>
        </el-menu-item>
        <el-sub-menu index="2">
          <template #title>文件</template>
          <el-menu-item index="2-1">item one</el-menu-item>
          <el-menu-item index="2-2">item two</el-menu-item>
          <el-menu-item index="2-3">item three</el-menu-item>
          <el-sub-menu index="2-4">
            <template #title>item four</template>
            <el-menu-item index="2-4-1">item one</el-menu-item>
            <el-menu-item index="2-4-2">item two</el-menu-item>
            <el-menu-item index="2-4-3">item three</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
        <el-menu-item index="3">编辑</el-menu-item>
        <el-menu-item index="4">查看</el-menu-item>
        <el-menu-item index="5">帮助</el-menu-item>
      </el-menu>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-scrollbar>
          <el-menu :default-openeds="['1', '2']">
            <el-sub-menu index="1">
              <template #title>
                <el-icon>
                  <setting />
                </el-icon>设置
              </template>
              <router-link to="/exp-settings">
                <el-menu-item index="1-1">
                  实验设置
                </el-menu-item>
              </router-link>
              <router-link to="/arena-settings">
                <el-menu-item index="1-2">
                  区域设置
                </el-menu-item>
              </router-link>
              <router-link to="/detection-settings">
                <el-menu-item index="1-3">
                  检测设置
                </el-menu-item>
              </router-link>
              <!-- <router-link to="/trial-control-settings">
                <el-menu-item index="1-4">
                  试验控制
                </el-menu-item>
              </router-link> -->
              <router-link to="/trial-list">
                <el-menu-item index="1-5">
                  试验列表
                </el-menu-item>
              </router-link>

            </el-sub-menu>
            <el-sub-menu index="2">
              <template #title>
                <el-icon>
                  <Memo />
                </el-icon> Acquisition
              </template>
            </el-sub-menu>
            <el-sub-menu index="3">
              <template #title>
                <el-icon>
                  <DataAnalysis />
                </el-icon>结果分析
              </template>
              <router-link to="/detection-settings">
                <el-menu-item index="1-3">
                  检测设置
                </el-menu-item>
              </router-link>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
        <el-footer>
        </el-footer>
      </el-container>
    </el-container>



  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'

const activeIndex = ref('1')
const activeIndex2 = ref('1')
const item = {
  date: '2016-05-02',
  name: 'Tom',
  address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))
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