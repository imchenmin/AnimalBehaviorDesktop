'use strict';
// 避免在Electron打包的时候找不到asar之外的ffmpeg路径。const ffmpeg = require('fluent-ffmpeg');
const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path.replace('app.asar', 'app.asar.unpacked');
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
        this._ffmpegCommandTop;
        this._ffmpegCommandSide;
        this._videoServerTop;
        this._videoServerSide;
        this._top = props._top;
        this._side = props._side;
        this._saveVideoPath = props._saveVideoPath;
    }

    stopFFmpegCommand() {
        let enableDestroy = require('server-destroy');

        if (this._ffmpegCommandTop && this._top) {
            // this._ffmpegCommandTop.ffmpegProc.stdin.write("q\n");
            // this._ffmpegCommandTop.kill()
        }

        if (this._ffmpegCommandSide && this._side) {
            // this._ffmpegCommandSide.ffmpegProc.stdin.write('q\n');
            this._ffmpegCommandSide.kill()
        }

        this._videoServerTop.shutdown(function(err) {
            if (err) {
                return console.log('shutdown failed', err.message);
            }
            console.log('Everything is cleanly shutdown.');
        });
        this._videoServerSide.shutdown(function(err) {
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
        console.log("top camera start", this._top, this._saveVideoPath)
        if (!this._videoServerTop && this._top) {
            // this.stopFFmpegCommand();
            let videoCodec = 'libx264'
            console.log("top camera start")
            this._videoServerTop = http.createServer((request, response) => {
                let bufferStream = new stream.PassThrough();
                this._ffmpegCommandTop = ffmpeg()
                    .input('video=USB GS CAM')
                    .inputOption('-f', 'dshow')
                    .output(this._saveVideoPath.saveVideoPathTop)
                    .videoCodec('copy')
                    .output(bufferStream)
                    .videoCodec(videoCodec)
                    .format('mp4')
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
            this._videoServerTop = require('http-shutdown')(this._videoServerTop);

            this._videoServerTop.listen(8889);

        }
        if (!this._videoServerSide && this._side) {
            // this.stopFFmpegCommand();
            let videoCodec = 'libx264'
            console.log("side camera start")
            this._videoServerSide = http.createServer((request, response) => {
                let bufferStream2 = new stream.PassThrough();
                this._ffmpegCommandSide = ffmpeg()
                    .input('video=KS2A293-D')
                    .inputOption('-f', 'dshow')
                    .output(this._saveVideoPath.saveVideoPathSide)
                    .outputOptions([
                        '-vcodec copy'
                    ])
                    .output(bufferStream2)
                    .videoCodec(videoCodec)
                    .format('mp4')
                    .outputOptions(
                        '-movflags', 'frag_keyframe+empty_moov+faststart',
                        '-g', '18')
                    .on('progress', function(progress) {
                        console.log('time-side: ' + progress.timemark);
                    })
                    .on('error', function(err) {
                        console.log('An error occurred:  2' + err.message);
                    })
                    .on('end', function() {
                        console.log('Processing finished 2 !');
                    })
                    .run()
                bufferStream2.pipe(response);
            })
            this._videoServerSide = require('http-shutdown')(this._videoServerSide);

            this._videoServerSide.listen(8890);
        }
    }
}