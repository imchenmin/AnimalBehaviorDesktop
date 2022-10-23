import { defineStore } from 'pinia'
import { ref } from 'vue'
import {ProcessingObject, pstatus, ptype} from '../objects/ProcessingObject'

export const useStatusStore =  defineStore('status', () => {
    const processingList = ref<Array<ProcessingObject>>()

    async function fetchInfo() {
        
    }
    return {
        processingList, fetchInfo
    }
})