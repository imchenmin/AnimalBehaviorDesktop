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
import VueGoodTablePlugin from 'vue-good-table-next'
import 'vue-good-table-next/dist/vue-good-table-next.css'

const app = createApp(App);
app.use(ElementPlus);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(VueGoodTablePlugin);
app.use(router)
app.use(pinia)

app.mount("#app");
