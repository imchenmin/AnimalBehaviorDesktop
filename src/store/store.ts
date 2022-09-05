// 作为根状态保管器。
import { defineStore } from 'pinia'
const Datastore = require('nedb');

export const useVersionStore = defineStore('version', {
    state: () => {
        return {
            author: 'chenmin',
            email: 'zbcmb@outlook.com',
            softwareName: "具安动物行为分析",
            DeviceID: "demo"
        }
    },
    persist: true
})
export const useDefaultSetting = defineStore('settings', {
    state: () => {
        return {
            default_parent_folder: ""
        }
    },
    actions: {
        getHomeDir() {
            let os=require('os');
            let homedir=os.homedir();
            this.default_parent_folder = homedir;
            console.log(homedir)
        }
    },
    persist: true
})
export const useDatasetStore = defineStore('db', {
    state: () => {
        return {
            default_db: new Datastore({ filename: 'history.json', autoload: true }),
            current_project_db: ""
        }
    },
    actions: {
        getHomeDir() {
            let os=require('os');
            let homedir=os.homedir();
            this.default_parent_folder = homedir;
            console.log(homedir)
        }
    },
    persist: true
})
export default {useVersionStore, useDefaultSetting}