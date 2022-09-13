'use strict';
const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;
const ffmpeg = require('fluent-ffmpeg');
ffmpeg.setFfmpegPath(ffmpegPath);
const http = require('http');

function getParam(url, key) {
    var param = new Object();
    var item = new Array();
    var urlList = url.split("?");
    var req;
    if (urlList.length == 1) {
        req = urlList[0];
    } else {
        req = urlList[1];
    }
    var list = req.split('&');
    for (var i = 0; i < list.length; i++) {
        item = list[i].split('=');
        param[item[0]] = item[1];
    }
    return param[key] ? param[key] : null;
}

export default class CameraServer {

    constructor(props) {
        this._ffmpegCommand;
        this._videoServer;
        this._saveVideoPath = props._saveVideoPath;
        this._camera_name = props.camera_name;
        this._port = props._port
    }

    stopFFmpegCommand() {

        if (this._ffmpegCommand) {
            // this._ffmpegCommand.ffmpegProc.stdin.write("q\n");
            // this._ffmpegCommand.kill()
        }

 
        this._videoServer.shutdown(function(err) {
            if (err) {
                return console.log('shutdown failed', err.message);
            }
            console.log('Everything is cleanly shutdown.');
        });
      
        console.log("stopFFMPEG")




    }
    createCameraServer() {
        // top camera misc
        let enableDestroy = require('server-destroy');
        let fs = require('fs')
        let stream = require('stream')
        console.log("camera start", this._saveVideoPath)
        if (!this._videoServer) {
            let videoCodec = 'libx264'
            console.log("top camera start")
            this._videoServer = http.createServer((request, response) => {
                let bufferStream = new stream.PassThrough();
                this._ffmpegCommand = ffmpeg()
                    .input('video='+this._camera_name)
                    .inputOption('-f', 'dshow')
                    .output(this._saveVideoPath.saveVideoPath)
                    .videoCodec('copy')
                    .output(bufferStream)
                    .videoCodec(videoCodec)
                    .format('mp4')
                    .fps(30)
                    .outputOptions(
                        '-movflags', 'frag_keyframe+empty_moov+faststart',
                        '-g', '18')
                    .on('progress', function(progress) {
                        console.log('time: ' + progress.timemark);
                    })
                    .on('error', function(err) {
                        console.log('An error occurred: ' + err.message);
                    })
                    .on('end', function() {
                        console.log('Processing finished !');
                    })
                    .run()
                bufferStream.pipe(response);
            })
            this._videoServer = require('http-shutdown')(this._videoServer);

            this._videoServer.listen(this._port);
        }
    }
}

let cameraJob = new cameraJob(argv[1])
cameraJob.createCameraServer()

process.on("message", (e)=>{
    if (e == 'stop') {
        cameraJob.stopFFmpegCommand()
        process.exit()
    }
})