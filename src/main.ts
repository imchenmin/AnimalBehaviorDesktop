import { createApp } from "vue";

import App from "./App.vue";


import 'uno.css'
//import element plus
import "~/styles/index.scss";
import "element-plus/theme-chalk/src/message.scss"
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

// import vue-router
import router from "./routers"

// import pinia
import { createPinia } from 'pinia'
const pinia = createPinia()

// import vue-good-table
// import pinia persistedstate
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'


// import echarts
import ECharts from 'vue-echarts'
import "echarts"

const app = createApp(App);
app.use(ElementPlus);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router)
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.component('v-chart', ECharts)
app.mount("#app")

const exec = require('child_process').exec;
// 异步执行
exec('C:\\Users\\Gianttek\\Anaconda3\\envs\\dlc-gpu\\python.exe C:\\Users\\Gianttek\\Anaconda3\\envs\\dlc-gpu\\backend\\main_flask.py',function(error, stdout, stderr){
    if(error) {
        console.info('stderr : '+stderr);
    }
    console.log('exec: ' + stdout);
})