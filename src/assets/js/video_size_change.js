var canvas = document.getElementById('canvas');
var canvaslist = document.getElementById('canvaslist');
var vv = document.getElementById('video_id');
var mb = document.getElementById('main');
var cb = document.getElementById('control_bar');
var durationTimer = document.querySelector('.duration_timer');
var playBtn = document.querySelector('.play_pause');
let {totalT,presentT} = {totalT:0,presentT:0};
vv.addEventListener('canplaythrough',function(){

        console.log("Height: " + vv.videoHeight + ", Width: " + vv.videoWidth);
        vv.width = vv.videoWidth;
        vv.height = vv.videoHeight;
        mb.style.width = vv.videoWidth+"px";
        mb.style.height = vv.videoHeight+"px";
        console.log("Height: " + mb.style.width + ", Width: " + mb.style.height);
        canvas.style.width = vv.videoWidth+"px";
        canvas.style.height = vv.videoHeight+"px";
        canvas.width = vv.videoWidth;
        canvas.height = vv.videoHeight;
        cb.style.left = "auto";
        cb.style.width = vv.videoWidth+"px";
        cb.children[1].style.width = vv.videoWidth-210+"px";
        totalT = vv.duration;
        videoDuration = formatTime(totalT);
        durationTimer.innerHTML = videoDuration;
        // document.getElementById('t').style.marginLeft =vv.videoWidth/2-260;
        // document.getElementById('a').style.marginLeft =vv.videoWidth/2-260;
        // document.getElementById('addcanvas').style.marginLeft = vv.videoWidth/2-260;

        });
vv.addEventListener('timeupdate',function(){
    presentT = this.currentTime;
    var videoCurrent = formatTime(presentT);
    progressTimer.innerHTML = videoCurrent;
    var percent = presentT/totalT*100;
    progress.style.width = percent+'%';
    if (percent==0 || percent==100){
        playBtn.classList.add('fa-play');
        playBtn.classList.remove('fa-pause');
    }
})