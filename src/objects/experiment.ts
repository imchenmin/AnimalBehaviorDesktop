class ExperiemntObj {
    description:string;
    name: string;
    analysis_method: string;
    folder_path: string;
    date: Date;
    record_mouse_info: boolean;
    mouse_gender: string;
    mouse_genetype: string;
    mouse_dob: Date;
    tracking_mouse_number: number;
    detection_behavior_kinds: Array<string>;
    _id: string;
    record_state: boolean;
    tracking_state: boolean;
    detection_state: boolean;
    constructor() {
        this.record_state = false;
        
    }
}
export default ExperiemntObj