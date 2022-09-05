import { defineStore } from 'pinia'
const Datastore = require('nedb');
import path from 'path'
import ExperiemntObj from '../objects/experiment'
export const useExperimentsStore = defineStore('experiments', {
    state: () => {
        return {
            current_project_id: -1,
            project_config_list: [],
            opened_project: new Array<ExperiemntObj>,
        }
    },
    persist: true,
    actions: {
        loadProject() {
            this.opened_project  = []
            let fs = require("fs")
            for ( let i of this.project_config_list) {
                fs.exists(i,  (exists) => {
                    if (!exists) {
                        console.log("project not found", i)
                    } else {
                        const db =  new Datastore({filename: i, autoload: true})
                        db.find({}, (err, docs)=> {
                            if (!err) {
                                this.opened_project.push(docs[0])
                            }else {
                                console.log("project database load error",  i)
                            }
                        })
                    }
                })
                
            }

        },
        addProject(payload: ExperiemntObj) {
            this.project_config_list.push(path.join(payload.folder_path, 'project.json'))
            this.opened_project.push(payload)
            const db = new  Datastore({filename: path.join(payload.folder_path, 'project.json'), autoload: true})
            db.insert(payload)
            return true
        },
        closeProject() {
            this.opened_project = null
        }

    }
})
export default useExperimentsStore