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

import VueSocketIO from 'vue-3-socket.io'
import io from 'socket.io-client';
const socketio = new VueSocketIO({
    debug: true,
    connection: io('http://127.0.0.1:8867',{ transports : ['websocket'] }),
});
const app = createApp(App);
app.use(ElementPlus);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router)
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(socketio)
app.component('v-chart', ECharts)
app.mount("#app")

const exec = require('child_process').exec;
// 异步执行
exec('C:\\Users\\Gianttek\\Anaconda3\\envs\\dlc-gpu\\python.exe C:\\Users\\Gianttek\\Anaconda3\\envs\\dlc-gpu\\backend\\main_flask.pyc',function(error, stdout, stderr){
    if(error) {
        console.info('stderr : '+stderr);
    }
    console.log('exec: ' + stdout);
})