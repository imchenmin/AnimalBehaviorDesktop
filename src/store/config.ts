import { defineStore } from 'pinia'

export const useConfigureStore = defineStore('config', {
    state: () => {
        return {
            serverApiUrl: 'https://api.vxetable.cn/demo/',
        }
    },
    persist: true
})
export default useConfigureStore