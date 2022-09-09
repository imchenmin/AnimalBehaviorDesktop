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
        this._videoSourceInfo;
        this._ffmpegCommandTop;
        this._ffmpegCommandSide;
        this._videoServerTop;
        this._videoServerSide;
        this._top=props._top;
        this._side=props._side;
        this._saveVideoPath;
    }

    set videoSourceInfo(info) {
        this._videoSourceInfo = info;
    }

    get videoSourceInfo() {
        return this._videoSourceInfo;
    }

    stopFFmpegCommand() {
        if (this._ffmpegCommandTop && this._top) {
            this._ffmpegCommandTop.ffmpegProc.stdin.write('q');
        }
        if (this._ffmpegCommandSide && this._side) {
            this._ffmpegCommandSide.ffmpegProc.stdin.write('q');
        }
    }
    createCameraServer() {
        // top camera misc
        console.log("top camera start",this._top)
        if (!this._videoServerTop && this._top) {
            this.stopFFmpegCommand();
            let videoCodec = 'libx264'
            console.log("top camera start")
            this._videoServerTop = http.createServer((request, response) => {
            this._ffmpegCommandTop = ffmpeg()
                .input('video=USB webcam')
                .inputOption('-f','dshow')
                .videoCodec(videoCodec)
                .format('mp4')
                .outputOptions(
                    '-movflags', 'frag_keyframe+empty_moov+faststart',
                    '-g', '18')
                .on('progress', function (progress) {
                    console.log('time: ' + progress.timemark);
                })
                .on('error', function (err) {
                    console.log('An error occurred: ' + err.message);
                })
                .on('end', function () {
                    console.log('Processing finished !');
                })
                let videoStreamTop = this._ffmpegCommandTop.pipe();
                videoStreamTop.pipe(response);
            }).listen(8889);
        }
        if (!this._videoServerSide && this._side) {
            this.stopFFmpegCommand();
            let videoCodec = 'libx264'
            console.log("side camera start")
            this._videoServerSide = http.createServer((request, response) => {
            this._ffmpegCommandSide = ffmpeg()
                .input('video=KS2A293-D')
                .inputOption('-f','dshow')
                .videoCodec(videoCodec)
                .format('mp4')
                .outputOptions(
                    '-movflags', 'frag_keyframe+empty_moov+faststart',
                    '-g', '18')
                .on('progress', function (progress) {
                    console.log('time-side: ' + progress.timemark);
                })
                .on('error', function (err) {
                    console.log('An error occurred: ' + err.message);
                })
                .on('end', function () {
                    console.log('Processing finished !');
                })
                let videoStreamSide = this._ffmpegCommandSide.pipe();
                videoStreamSide.pipe(response);
            }).listen(8890);
        }
    }
}