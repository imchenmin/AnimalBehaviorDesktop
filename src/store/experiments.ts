import { defineStore } from 'pinia'

export const useExperimentsStore = defineStore('experiments', {
    state: () => {
        return {
            location: 'chenmin',
            descripttion: "",
            name: "",
            video_sorce_type: "",
            video_sorce_uri: "",
            unit_of_distance: "", //单位制 
            unit_of_time: "",
            unit_of_degree: "",
            behavior_unit: ""
        }
    },
    persist: true
})
export default useExperimentsStore