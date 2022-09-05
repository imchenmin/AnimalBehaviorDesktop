var videoObj = document.getElementById('video_id')
var playBtn = document.querySelector('.play_pause')
var progressTimer = document.querySelector('.progress_timer')
var durationTimer = document.querySelector('.duration_timer')
var progress = document.querySelector('.progress')
var player = document.querySelector('.control')
var expand = document.querySelector('.expand')
var innerbar = document.getElementById('control_bar').children[1]
playBtn.addEventListener('click', function(){
    if(videoObj.paused){
        // 如果视频处于播放状态
        videoObj.play()
        this.classList.remove('fa-play')
        this.classList.add('fa-pause')
    }else{
        videoObj.pause()
        this.classList.add('fa-play')
        this.classList.remove('fa-pause')
    }
})
innerbar.addEventListener('click', function(e){
    if(videoObj.paused || videoObj.ended){
            videoObj.play()
            playBtn.classList.remove('fa-play')
            playBtn.classList.add('fa-pause')
            enhanceVideoSeek(e);
    }
    else{
            enhanceVideoSeek(e);
    }
    
    
})
function enhanceVideoSeek(e){
    //videoObj.pause()
    var length = e.pageX - innerbar.offsetLeft-player.offsetLeft;
    var percent = length / innerbar.offsetWidth;
    progress.style.width = percent*innerbar.style.width+'px';
    videoObj.currentTime = percent * videoObj.duration;
  }


expand.addEventListener('click',function(){
    videoObj.webkitRequestFullScreen()
})