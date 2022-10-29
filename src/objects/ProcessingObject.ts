enum ptype {
    DOWNLOADING=1,
    ANALYSIS,

}
enum pstatus {
    WAITTING=1,
    PROCESSING,
    CANCELED,
    DONE
}
class ProcessingObject {
    ptype: ptype
    project_id: string
    progress: number
    status:pstatus
    info: string
    project_front_end_id: string
    project_path: string
    constructor(project_id:string,ptype: ptype, project_front_end_id, project_path) {
        this.ptype = ptype
        this.project_id = project_id
        this.progress = 0.0
        this.status = pstatus.WAITTING
        if (project_front_end_id == '') {
            // 丢出警报
        } else {
            this.project_path = project_path
        }
    }

}
export { ProcessingObject, pstatus, ptype }