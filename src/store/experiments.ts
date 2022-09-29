import { defineStore } from 'pinia'
const Datastore = require('nedb');
import path from 'path'
import ExperiemntObj from '../objects/experiment'
import ConfigObject from '../objects/configObject';
export const useExperimentsStore = defineStore('experiments', {
    state: () => {
        return {
            current_project_id: -1,
            opened_project: new Array<ExperiemntObj>(),
            config: new ConfigObject,
        }
    },
    actions: {
        async loadProject() {
            const settings_db = new Datastore({filename: "settings.json", autoload: true})
            settings_db.find({}, async (err, docs)=>{
                if (!err) {
                    if (docs[0]) {
                        this.config = docs[0] as ConfigObject;
                    } else {
                        settings_db.insert(this.config, (err,newDoc)=> {
                            console.log("insert settings db", newDoc)
                            this.config._id = newDoc._id;
                        })                    }
                    console.log(this.config)
                } else {
                    console.log("err",err);
                }
                let fs = require("fs")
                let util = require('util')
                let count = 0
                for (let i = 0; i < this.config.openedProjectList.length; ++i) {
                    let exists =  await util.promisify(fs.exists)(this.config.openedProjectList[i])
                    if (exists) {
                        const db = new Datastore({ filename: this.config.openedProjectList[i], autoload: true })
                        db.find({}, async (err, docs) => {
                            if (!err) {
                                let current_exp = docs[0] as ExperiemntObj
                                let capture =  await util.promisify(fs.exists)(path.join(this.config.openedProjectList[i],'..', 'video.mkv'))
                                current_exp.record_state=capture
                                this.opened_project.push(current_exp)
                            } else {
                                console.log("project database load error", this.config.openedProjectList[i])
                            }
                        })
                    } else {
                        
                        this.config.openedProjectList.splice(i,1)
                    }   
                    count++
                }
                console.log("project config list",this.config.openedProjectList);
                console.log("open list",this.opened_project);
    
                console.log("load finish")
            })

        },
        async addProject(payload: ExperiemntObj) {
            const db = new Datastore({ filename: path.join(payload.folder_path, 'project.json'), autoload: true })
            await db.insert(payload, (err,newDoc)=> {
                this.config.openedProjectList.push(path.join(payload.folder_path, 'project.json'))
                this.opened_project.push(newDoc)
            })
            this.updateConfig()
        },
        async updateProject(payload: ExperiemntObj) {
            const db = new Datastore({ filename: path.join(payload.folder_path, 'project.json'), autoload: true })
            await db.update({_id: payload._id},payload, (err,newDoc) => {
                console.log('update', newDoc)
            })
        },
        async updateConfig() {
            const db = new Datastore({ filename: "settings.json", autoload: true })
            await db.update({_id: this.config._id},this.config, (err,newDoc) => {
                console.log('update', newDoc)
            })
        },
        closeProject() {
            this.opened_project = null
        },
        get_from_id(idx: string) {
            console.log(idx)
            return this.opened_project.find(element => element._id == idx)
        }

    }
})
export default useExperimentsStore