class ConfigObject {
    last_openDate: Date;
    openedProjectList: Array<string>;
    cameraList: Array<CameraObject>;
    _id: string;

    constructor() {
        this.openedProjectList = [];
    }   
}
export default ConfigObject