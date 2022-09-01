// 作为根状态保管器。
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
    state: () => {
        return {
            author: 'chenmin',
            email: 'zbcmb@outlook.com',
            softwareName: "具安动物行为分析"
        }
    }
})