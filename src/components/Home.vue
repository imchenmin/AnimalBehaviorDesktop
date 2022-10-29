<template lang="">
  <H2>
    使用说明
  </H2>
  
</template>
<script lang="ts" setup>
import useStore from '../store'
const { settings } = useStore();
// let ipcRenderer = require('electron').ipcRenderer;
// ipcRenderer.send("listDshowDevices")
const showSetting = () => {
  settings.toggleShow()
  console.log(settings.showSettingWidgt)
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
.Home {
  
}
</style>