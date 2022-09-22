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

export default class VideoServer {

    constructor(props) {
        this._videoServer;
        this._videoSourceInfo;
        this._ffmpegCommand;
        this.is_run = true
    }

    set videoSourceInfo(info) {
        this._videoSourceInfo = info;
    }

    get videoSourceInfo() {
        return this._videoSourceInfo;
    }

    killFfmpegCommand() {
        if (this.is_run == false) {
            return
        }
        this.is_run = false
        if (this._ffmpegCommand) {
            this._ffmpegCommand.kill();
        }
        this._videoServer.shutdown(function(err) {
            if (err) {
                return console.log('shutdown failed', err.message);
            }
            console.log('Everything is cleanly shutdown.');
            // process.exit()

        });
    }

    createServer() {
        if (!this._videoServer && this.videoSourceInfo) {
            this._videoServer = http.createServer((request, response) => {
                console.log("on request", request.url);
                var startTime = parseInt(getParam(request.url, "startTime"));
                console.log("starttime", startTime, request.url)
                let videoCodec = this.videoSourceInfo.checkResult.videoCodecSupport ? 'copy' : 'libx264';
                this.killFfmpegCommand();
                this._ffmpegCommand = ffmpeg()
                    .input(this.videoSourceInfo.videoSourcePath)
                    .nativeFramerate()
                    .videoCodec(videoCodec)
                    .format('mp4')
                    .seekInput(startTime)
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
                let videoStream = this._ffmpegCommand.pipe();
                videoStream.pipe(response);
            })
            this._videoServer = require('http-shutdown')(this._videoServer);
            this._videoServer.listen(8888);
        }
    }
}