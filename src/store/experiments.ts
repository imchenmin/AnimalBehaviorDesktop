import { defineStore } from 'pinia'
const Datastore = require('nedb');
import path from 'path'
import ExperiemntObj from '../objects/experiment'
import ConfigObject from '../objects/configObject';
import { ElMessage } from 'element-plus'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router';
let fs = require("fs")
let util = require('util')

export const useExperimentsStore = defineStore('experiments', () => {
    const router = useRouter()
    const opened_project = ref<Array<ExperiemntObj>>(new Array<ExperiemntObj>());
    const config = ref<ConfigObject>()
    function loadProject() {
        const settings_db = new Datastore({filename: "settings.json", autoload: true})
        settings_db.find({}, async (err, docs)=>{
            if (!err) {
                if (docs[0]) {
                    config.value = docs[0] as ConfigObject;
                } else {
                    settings_db.insert(config, (err,newDoc)=> {
                        console.log("insert settings db", newDoc)
                        config.value._id = newDoc._id;
                    })                    }
                console.log(config)
            } else {
                console.log("err",err);
            }

            let count = 0
            for (let i = 0; i < config.value.openedProjectList.length; ++i) {
                let exists =  await util.promisify(fs.exists)(config.value.openedProjectList[i])
                if (exists) {
                    const db = new Datastore({ filename: config.value.openedProjectList[i], autoload: true })
                    db.find({}, async (err, docs) => {
                        if (!err) {
                            let current_exp = docs[0] as ExperiemntObj
                            let capture =  await util.promisify(fs.exists)(path.join(config.value.openedProjectList[i],'..', 'video.mkv'))
                            current_exp.record_state=capture
                            opened_project.value.push(current_exp)
                        } else {
                            console.log("project database load error", config.value.openedProjectList[i])
                        }
                    })
                } else {
                    config.value.openedProjectList.splice(i,1)
                }   
                count++
            }

            console.log("load finish")
        })
    }
    async function addProject(payload: ExperiemntObj) {
        const db = new Datastore({ filename: path.join(payload.folder_path, 'project.json'), autoload: true })
        await db.insert(payload, (err,newDoc)=> {
            this.config.openedProjectList.push(path.join(payload.folder_path, 'project.json'))
            this.opened_project.push(newDoc)
        })
        this.updateConfig()
    }
    function get_from_id(idx: string) {
        console.log(idx)
        return this.opened_project.find(element => element._id == idx)
    }
    async function importProject(payload: string) {
        // 文件名检测
        if (path.basename(payload) != 'project.json') {
            // 提示通知
            ElMessage({
                message: "项目配置文件应为project.json",
            })
            return;
        }
        const db = new Datastore({ filename: payload, autoload: true })
        // 类型检查
        await db.find({}, async(err, docs) => {
            if (!err) {

                let current_exp = docs[0] as ExperiemntObj;
                console.log(current_exp, typeof current_exp)
                if (this.config.openedProjectList.indexOf(payload) == -1) {
                    this.config.openedProjectList.push(payload)
                    let capture =  await util.promisify(fs.exists)(path.join(payload,'..', 'video.mkv'))
                    current_exp.record_state=capture
                    this.opened_project.push(current_exp)
                    this.updateConfig()
                    ElMessage({
                        message: "项目导入成功！",
                    })
                router.push("/project/" + current_exp._id)
                } else {
                    ElMessage({
                        message: "不重复导入项目！",
                    })
                }
            }
        })
    }
    function updateConfig() {
        const db = new Datastore({ filename: "settings.json", autoload: true })
        db.update({_id: config.value._id},config.value, (err,newDoc) => {
            console.log('update', newDoc)
        })
    }
    async function updateProject(payload: ExperiemntObj) {
        const db = new Datastore({ filename: path.join(payload.folder_path, 'project.json'), autoload: true })
        await db.update({_id: payload._id},payload, (err,newDoc) => {
            console.log('update', newDoc)
        })
    } 
    async function closeProject(project_id: String) {
        // 关闭指定的项目，从列表中移除
        for (let i = 0; i < config.value.openedProjectList.length; ++i) {
            console.log(this.opened_project)
            if (this.opened_project[i]._id == project_id) {
                this.config.openedProjectList.splice(i,1)
                this.opened_project.splice(i,1)
                console.log()
                updateConfig()
                ElMessage({message: "已成功关闭项目！"})
                router.push('/')
                return
            }
        }
    }

    return {opened_project, config, loadProject, addProject, get_from_id, importProject, updateConfig, updateProject, closeProject}
})
export default useExperimentsStore