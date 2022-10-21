import CameraObject from "./CameraObject";

class ConfigObject {
    last_openDate: Date;
    openedProjectList: Array<string>;
    cameraList: Array<CameraObject>;
    rtspSourceList: Array<CameraObject>; //alternativeName表示rtsp路径。以达到复用的目的
    _id: string;

    constructor() {
        this.openedProjectList = [];
        this.cameraList = [];
        this.rtspSourceList = [];
    }   
}
export default ConfigObject