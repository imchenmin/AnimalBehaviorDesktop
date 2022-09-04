import { createRouter, createWebHistory } from "vue-router";

// 引入
import Home from "~/components/Home.vue"

import ExperimentSetting from "~/components/ExperimentSetting.vue"
import ArenaSetting from "~/components/ArenaSetting.vue"
import TrialControlSetting from "~/components/TrialControlSetting.vue"
import TrialList from "~/components/TrialList.vue"
import DetectionResult from "~/components/DetectionResult.vue"

// 路由信息
let routes = [
  {
    path: "/",
    name: 'home',
    component: Home,
  },
  {
    path: "/exp-settings",
    name: "ExperimentSetting",
    component: ExperimentSetting
  },
  {
    path: "/arena-settings",
    name: "ArenaSetting",
    component: ArenaSetting
  },
  {
    path: "/trial-control-settings",
    name: "TrialControlSetting",
    component: TrialControlSetting
  },
  {
    path: "/trial-list",
    name: "TrialList",
    component: TrialList
  },
  {
    path: "/detection-result",
    name: "DetectionResult",
    component: DetectionResult
  },
];

// 路由器
// 1. 定义路由组件.
// 也可以从其他文件导入

// 2. 定义一些路由
// 每个路由都需要映射到一个组件。
// 我们后面再讨论嵌套路由。
// 3. 创建路由实例并传递 `routes` 配置
// 你可以在这里输入更多的配置，但我们在这里
// 暂时保持简单
const router = createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
  history: createWebHistory(), // HTML5模式
  routes,// `routes: routes` 的缩写
});

export default router;