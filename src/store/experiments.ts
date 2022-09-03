import { defineStore } from 'pinia'
import db from '../nedb'

export const useExperimentsStore = defineStore('experiments', {
    state: () => {
        return {
            location: 'chenmin',
            descripttion: "",
            name: "",
            analysis_method: "",
            records: [],
            loading: false,
        }
    },
    persist: true,
    actions: {
        fetchAllRecords() {
            this.loading = true;
            db.find({}, (err, records) => {
                this.records = records;
            });
            this.loading = false;
        },
        addRecord(payload: Object) {
            this.loading = true;
            db.insert(payload, (err, record) => {
                this.records.push(record);
            });
            this.loading = false;
        }
    }
})
export default useExperimentsStore