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
import router from "~/router/index"

// import pinia
import { createPinia } from 'pinia'
const pinia = createPinia()


const app = createApp(App);
app.use(ElementPlus);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router)
app.use(pinia)

app.mount("#app");
