import { defineStore } from 'pinia'
const Datastore = require('nedb');
import path from 'path'
export const useExperimentsStore = defineStore('experiments', {
    state: () => {
        return {
            descripttion: "",
            name: "",
            analysis_method: "",
            records: [],
            loading: false,
            folder_path: ".",
            date: new Date(),
            record_mouse_info: false,
            mouse_gender: '',
            mouse_genetype: '',
            mouse_dob: new Date(),
            tracking_mouse_number: 1
        }
    },
    persist: true,
    getters: {
        db: (state) => new Datastore({ filename: path.join(state.folder_path,'records.pkg'), autoload: true })
    },
    actions: {
        fetchAllRecords() {
            this.loading = true;
            this.db.find({}, (err, records) => {
                this.records = records;
            });
            this.loading = false;
        },
        addRecord(payload: Object) {
            this.loading = true;
            this.db.insert(payload, (err, record) => {
                this.records.push(record);
            });
            this.loading = false;
        }
    }
})
export default useExperimentsStore