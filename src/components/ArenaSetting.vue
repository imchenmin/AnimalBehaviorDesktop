<template>
    <StepControl :_id="current_exp._id" :activate="2"></StepControl>
    <div id="main" style="border: solid black 1px; curssor: default; " ref="mainboard">
        <video ref="videoPlayerTop" class="video-js" style="position: absolute;"></video>
        <!-- <video id="video_id" preload  style="position: absolute;" data-setup="{}" ref="videoObj" type='video/mp4' :src="videoSrc">
        </video> -->
        <div id="canvaslist" style="position: absolute;" ref="canvaslist">
            <canvas id="canvas" ref="canvas"></canvas>
        </div>
    </div>
    <div class="control" id="control_bar" ref = "control_bar">
        <div class="fa fa-play play_pause" ref = "play_btn"></div>
        <div>
                <span class="progress"></span>
        </div>
        <div class="timer">
                <span class="progress_timer">00:00:00</span>/
                <span class="duration_timer">00:00:00</span>
        </div>
        <div class="fa fa-expand expand"></div>
    </div>   
    
    <input type="button" class="el-button el-button--simple is-plain" value="开始标记" id="startmark" style="float:left; margin-top:10px;"/> 
    <input type="button" class="el-button el-button--simple is-plain" value="添加矩形" id="addrectangle" style="display: none; float:left; margin-top:10px;"/> 
    <input type="button" class="el-button el-button--simple is-plain" value="添加多边形" id="addcanvas" style="display: none; float:left; margin-top:10px;"/>
    <el-button-group style="margin-top:10px; margin-left:10px;" >
        <el-button type="simple" plain @click = "savemark" >保存标记</el-button>
        <el-button type="simple" plain @click="onUploadMark">上传已保存的标记</el-button>
    </el-button-group>
    <input type="file"  id="uploadbutton" style="display: none;" accept=".txt" ref="markInput" />    
    <input type="button" value="选择视频" style="display: none" @click="onSelectVideo" />
    <input type="file" id="file-uploader" style="margin-left:140; display: none;" accept="video/*" @change="selectvideo" ref="videoInput" />
    <el-form-item label="感兴趣的身体部位">
        <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll"                 
                    @change="handleCheckAllChange" style="margin-right:20px">全选</el-checkbox>                   
        <el-checkbox-group v-model="checkedParts" @change="handleCheckedPartsChange">
            <el-checkbox v-for="part in partsArr" :label="part" :key="part">{{part}}</el-checkbox>
        </el-checkbox-group>
    </el-form-item>
    <el-button-group>
        <el-button type="simple" plain @click="onRunit">根据当前标记进行分析</el-button>
        <input type="button" value="根据当前标记进行分析"  style="display: none" id="rundetect" ref="runItButton" />
        <el-button type="simple" plain @click="embyPot">查看结果</el-button>
    </el-button-group>
</template>
<script >
    let fs = window.require('fs');
    let ipcRenderer = require('electron').ipcRenderer;
    import { ElMessage, ElMessageBox } from 'element-plus'
    import "../assets/css/control_bar.css"
    import "../assets/css/font-awesome.min.css"
    import ExperiemntObj from '../objects/experiment'
    import useStore from '../store'
    import path from 'path'
    import videojs from 'video.js';
    import 'video.js/dist/video-js.css';

    const bodypartOptions = ['Body', 'Head', 'Tail', 'Nose'];
    export default {
        data(){
            return{
                videoname : "video",
                videopath : "",
                _id: this.$route.params._id,
                partsArr: bodypartOptions, //一共有多少个选项
                checkAll: true,
                checkedParts: bodypartOptions, //默认选中的值,这里是默认全选
                isIndeterminate: false,
            };
        },
        computed: {
            current_exp() {
                const { settings, experiments } = useStore();
                this.videopath = experiments.get_from_id(this._id).folder_path;
                return experiments.get_from_id(this._id);
            },
            videoSrc() {
                return  this.current_exp.folder_path + "/"+this.videoname+".mp4";
            }
        },
        mounted() {
            var __this = this;
            //video player init
            const videoPlayerTop = __this.$refs.videoPlayerTop;
            var playerTop = null;
            let {totalT,presentT} = {totalT:0,presentT:0};
            var playBtn = document.querySelector('.play_pause')
            var progressTimer = document.querySelector('.progress_timer')
            var durationTimer = document.querySelector('.duration_timer')
            var progress = document.querySelector('.progress')
            var player = document.querySelector('.control')
            var expand = document.querySelector('.expand')
            var innerbar = document.getElementById('control_bar').children[1]
            function formatTime(t){
                var h = parseInt(t/3600)
                h = h<10?'0'+h:h 
                var m = parseInt(t%3600/60)
                m = m<10?'0'+m:m
                var s = parseInt(t%60)
                s = s<10?'0'+s:s
                return h+':'+m+':'+s
            } 
            ipcRenderer.send('playVideoFromFile', path.join(__this.current_exp.folder_path, 'video.mkv'), path.join(__this.current_exp.folder_path, 'video1.mkv'));
            ipcRenderer.on('videoServerReady', (event, message) => {
                console.log(message, "message")
                let videoOptionsTop = {
                    width: 800,
                    height: 450,
                    preload: 'metadata',
                    sources: [
                        {
                            src: 'http://127.0.0.1:8888?startTime=0',
                            type: 'video/mp4'
                        }
                    ],
                    techOrder: ['StreamPlay'],
                    StreamPlay: { duration: message.duration }
                }
                console.log(videoPlayerTop)
                playerTop = videojs(videoPlayerTop, videoOptionsTop, () => {
                    playerTop.log('onPlayerReady', this);
                });
                console.log('videoServerReady-render:', message)
                playerTop.load()
                //playerTop.play()
                playerTop.on('loadedmetadata',function(){
                    //console.log('loadedmetadata')
                    //console.log(playerTop.duration()) 
                    let durationTimer = document.querySelector('.duration_timer');
                    durationTimer.innerHTML = formatTime(playerTop.duration());
                    totalT = playerTop.duration();
                })
                playerTop.on('timeupdate',function(){
                    presentT = playerTop.currentTime();
                    var videoCurrent = formatTime(presentT);
                    progressTimer.innerHTML = videoCurrent;
                    var percent = presentT/totalT*100;
                    progress.style.width = percent+'%';
                    if (percent==0 || playerTop.ended()){
                        playBtn.classList.add('fa-play');
                        playBtn.classList.remove('fa-pause');
                    }
                    // if (playerTop.ended()){
                    //     playerTop.currentTime=(0.1);
                    // }
                })
            });

            var isMove = false;
            function getDragAngle(event){
                var element = event.target;
                var startAngle = parseFloat(element.dataset.angle) || 0;
                var center = {
                    x: parseFloat(element.dataset.centerX) || 0,
                    y: parseFloat(element.dataset.centerY) || 0,
                };
                var angle = Math.atan2(center.y - event.clientY, center.x - event.clientX);
                return angle - startAngle;
            }
            function rotatedown(event){
                const element = event.target;
                const rect = element.getBoundingClientRect();
                element.dataset.centerX = rect.left + rect.width / 2;
                element.dataset.centerY = rect.top + rect.height / 2;
                element.dataset.angle = getDragAngle(event);
                isMove = true;
            }
            function rotateup(event){
                isMove = false;
                event.target.dataset.angle = getDragAngle(event);
            }
            function rotatemove(event){
                if (isMove) {
                        var angle = getDragAngle(event);
                        event.target.style.transform = 'rotate(' + angle + 'rad)';
                }
            }
            var Rect = { 
                            //当前正在画的矩形对象 
            obj: null, 
            //画布 
            container: null, 
            name: null,
            //初始化函数 
            init: function(containerId){ 
            Rect.container = document.getElementById(containerId); 
            if(Rect.container){ 
                    //鼠标按下时开始画
                Rect.container.onmousedown = null; 

            } 
            else{ 
            alert('You should specify a valid container!'); 
            } 
            }, 
            start: function(e){ 
            var e1 = e || window.event;
            var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
            var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
            var x = e1.pageX || e1.clientX + scrollX;
            var y = e1.pageY || e1.clientY + scrollY;
            //console.log(x);
            //console.log(y);
            var o = Rect.obj = document.createElement('div'); 
            o.style.position = "absolute"; 
            // mouseBeginX，mouseBeginY是辅助变量，记录下鼠标按下时的位置 

            o.style.left = x+"px";
            o.mouseBeginX = x; 
            o.style.top = y+"px";
            o.mouseBeginY = y; 
            //console.log(o.mouseBeginX);
            //console.log(o.mouseBeginY);
            o.style.height = 0; 
            o.style.width = 0; 
            o.style.border = "solid black 1px"; 
            //向o添加一个叉叉，点击叉叉可以删除这个矩形 
            var deleteLink = document.createElement('a'); 
            deleteLink.href="javascript:void(0);"; 
            deleteLink.onclick = function(){ 
                    Rect.container.removeChild(this.parentNode);  
            } 
            deleteLink.innerText = "x"; 
            //deleteLink
            var givename = document.createElement('a');
            var showname = document.createElement('a');
            givename.href = "javascript:void(0);";

            givename.onclick = function(){ 
                ElMessageBox.prompt("请输入此区域名称", '输入任意非中文字符', {
                    confirmButtonText: '确认',
                    cancelButtonText: '取消',
                    inputValue: o.getAttribute("name")})
                .then(({ value }) => {
                    //console.log(`input ${value}`)
                    o.setAttribute("name",value);
                    showname.innerText = value;
                })
                .catch(() => {
                    console.log('cancel input')
                })
            } 
            givename.innerText = "+";

            o.appendChild(deleteLink); 
            o.appendChild(givename); 
            o.appendChild(showname);
            o.setAttribute("class","rectangle");

            //把当前画出的对象加入到画布中 
            Rect.container.appendChild(o); 
            //处理onmousemove事件 
            Rect.container.onmousemove = Rect.move; 
            //处理onmouseup事件 
            Rect.container.onmouseup = Rect.end; 
            cancelbutton();
            }, 
            move: function(e){ 
            var e1 = e || window.event;
            var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
            var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
            var x = e1.pageX || e1.clientX + scrollX;
            var y = e1.pageY || e1.clientY + scrollY;
            var o = Rect.obj; 
            //dx，dy是鼠标移动的距离 
            var dx = x - o.mouseBeginX; 
            var dy = y - o.mouseBeginY; 
            //如果dx，dy <0,说明鼠标朝左上角移动，需要做特别的处理 
            if(dx<0){ 
            o.style.left = x; 
            } 
            if(dy<0){ 
            o.style.top = y; 
            } 
            o.style.height = Math.abs(dy)+"px"; 
            o.style.width = Math.abs(dx)+"px"; 
            }, 
            end: function(e){ 
                            //onmouseup时释放onmousemove，onmouseup事件句柄 
            Rect.container.onmousemove = null; 
            Rect.container.onmouseup = null; 
            Rect.obj = null; 
                //
                console.log(document.getElementsByClassName('rectangle').length);
                var rec =document.getElementsByClassName('rectangle')[document.getElementsByClassName('rectangle').length-1];
                rec.onmousedown=rotatedown;
                rec.onmousemove = rotatemove;
                rec.onmouseup = rotateup;
            },
            //辅助方法，处理IE和FF不同的事件模型 
            getEvent: function(e){ 
                if (typeof e == 'undefined'){ 
                        e = window.event; 
                } 
                //alert(e.x?e.x : e.layerX); 
                if(typeof e.x == 'undefined'){ 
                        e.x = e.layerX; 
                } 
                if(typeof e.y == 'undefined'){ 
                        e.y = e.layerY; 
                } 
                return e; 
            },
            };
            //poly
            var canvas = document.getElementById('canvas');
            canvas.width = 800;
            canvas.height = 450;
            var canvastodraw;
            var canvaslist = document.getElementById('canvaslist');
            var ctx = canvas.getContext('2d');
            var pointX, pointY;
            var pointArr = [];//存放坐标的数组

            ctx.strokeStyle = 'rgba(102,168,255,1)';//线条颜色
            ctx.lineWidth = 1;//线条粗细
            var oIndex = -1;//判断鼠标是否移动到起始点处，-1为否，1为是

            /*点击画点*/
            
            function clicktodraw(e){
                var element = e.target;
                var ctxx = element.getContext('2d');
                if (e.offsetX || e.layerX) {
                    pointX = e.offsetX == undefined ? e.layerX : e.offsetX;
                    pointY = e.offsetY == undefined ? e.layerY : e.offsetY;
                    var piX,piY;
                    if(oIndex > 0 && pointArr.length > 0){
                        piX = pointArr[0].x;
                        piY = pointArr[0].y;
                        //画点
                        makearc(ctxx, piX, piY, GetRandomNum(2, 2), 0, 180, 'rgba(102,168,255,1)');
                        pointArr.push({x: piX, y: piY});
                        canvasSave(pointArr,canvastodraw);//保存点线同步到另一个canvas
                        saveCanvas(canvastodraw);//生成画布
                    }else {
                        piX = pointX;
                        piY = pointY;
                        makearc(ctxx, piX, piY, GetRandomNum(2, 2), 0, 180, 'rgba(102,168,255,1)');
                        pointArr.push({x: piX, y: piY});
                        canvasSave(pointArr,canvastodraw);//保存点线同步到另一个canvas
                    }
                }
            }
            canvas.addEventListener('click',clicktodraw);
        
            function movemouse(e){
                var element = e.target;
                var ctxx = element.getContext('2d');
                if (e.offsetX || e.layerX) {
                    pointX = e.offsetX == undefined ? e.layerX : e.offsetX;
                    pointY = e.offsetY == undefined ? e.layerY : e.offsetY;
                    var piX,piY;
                    /*清空画布*/
                    ctxx.clearRect(0, 0, canvas.width, canvas.height);
                    /*鼠标下跟随的圆点*/
                    makearc(ctxx, pointX, pointY, GetRandomNum(4, 4), 0, 180, 'rgba(102,168,255,1)');

                    if (pointArr.length > 0) {
                        if((pointX > pointArr[0].x-15 && pointX < pointArr[0].x+15) && (pointY > pointArr[0].y-15 && pointY < pointArr[0].y+15)){
                            if(pointArr.length>1){
                                piX = pointArr[0].x;
                                piY = pointArr[0].y;
                                ctxx.clearRect(0, 0, canvas.width, canvas.height);
                                makearc(ctxx, piX, piY, GetRandomNum(4, 4), 0, 180, 'rgba(102,168,255,1)');
                                oIndex = 1;
                            }
                        }else {
                            piX = pointX;
                            piY = pointY;
                            oIndex = -1;
                        }
                        /*开始绘制*/
                        ctxx.beginPath();
                        ctxx.moveTo (pointArr[0].x, pointArr[0].y);
                        if (pointArr.length > 1){
                            for (var i = 1; i < pointArr.length; i++){
                                ctxx.lineTo(pointArr[i].x, pointArr[i].y);
                            }
                        }
                        ctxx.lineTo(piX, piY);
                        ctxx.fillStyle = 'rgba(161,195,255,0.1)';//填充颜色
                        ctxx.fill();//填充
                        ctxx.stroke();//绘制
                    }
                }
            }
            canvas.addEventListener('mousemove',movemouse);
                // 存储已生成的点线
            function canvasSave(pointArr, canvas){
                //console.log(canvas.getAttribute('id'));
                var ctxSave = canvas.getContext('2d');
                ctxSave.clearRect(0, 0, ctxSave.width, ctxSave.height);
                ctxSave.beginPath();
                if (pointArr.length > 1){
                    ctxSave.moveTo (pointArr[0].x, pointArr[0].y);
                    for (var i = 1; i < pointArr.length; i++){
                        ctxSave.lineTo(pointArr[i].x, pointArr[i].y);
                        ctxSave.fillStyle = 'rgba(161,195,255,0.1)';//填充颜色
                        //ctxSave.fill();
                        ctxSave.stroke();//绘制
                    }
                    ctxSave.closePath();
                }
            }

            /*生成画布 结束绘画*/
            function saveCanvas(canvas) {
                var ctxSave = canvas.getContext('2d');
                document.getElementById("canvas").style.display='none';
                ctxSave.closePath();//结束路径状态，结束当前路径，如果是一个未封闭的图形，会自动将首尾相连封闭起来
                //ctxSave.fill();//填充
                ctxSave.stroke();//绘制
                console.log(pointArr);
                var str = "";
                var xindex = 0;
                var yindex = 0;
                let canvasindextop = parseInt(mb.offsetTop);
                let canvasindexleft = parseInt(mb.offsetLeft);
                for (var i = 0; i<pointArr.length-1; i++){
                    str = str+pointArr[i].x+","+pointArr[i].y+";";
                    xindex+=pointArr[i].x;
                    xindex+=canvasindexleft;
                    yindex+=pointArr[i].y;
                    yindex+=canvasindextop;
                }
                xindex = xindex/(pointArr.length-1);
                yindex = yindex/(pointArr.length-1);
                canvas.dataset.points = str;   
                pointArr = [];
                //console.log(pointArr.length);
                var givename = document.createElement('a');
                var showname = document.createElement('a');
                //showname.style.pointerEvents='none';
                givename.href = "javascript:void(0);";
                givename.onclick = function(){ 
                    ElMessageBox.prompt("请输入此区域名称", '输入任意非中文字符', {
                        confirmButtonText: '确认',
                        cancelButtonText: '取消',
                        inputValue: canvas.getAttribute("name")})
                    .then(({ value }) => {
                        //console.log(`input ${value}`)
                        canvas.setAttribute("name",value);
                        showname.innerText = value;
                    })
                    .catch(() => {
                        console.log('cancel input')
                    })
                } 
                givename.style.position="absolute";
                givename.style.top = yindex+"px";
                givename.style.left = (xindex+12)+"px";
                givename.innerText = "+";
                var deleteLink = document.createElement('a'); 
                deleteLink.href="javascript:void(0);"; 
                deleteLink.onclick = function(){ 
                    canvaslist.removeChild(canvas); 
                    this.remove();
                    givename.remove();
                    showname.remove();
                } 
                deleteLink.style.position="absolute";
                deleteLink.style.top = yindex+"px";
                deleteLink.style.left = xindex+"px";
                deleteLink.innerText = "x";
                showname.style.position="absolute";
                showname.style.top = yindex+17+"px";
                showname.style.left = xindex+"px";
                mb.appendChild(deleteLink);
                mb.appendChild(givename);
                mb.appendChild(showname);
            }

            /*清空选区*/
            var canvas_index = 1;
            
            function addcanvas(){
                var canvastoadd = document.createElement('canvas');
                canvastoadd.setAttribute("class", "ud_canvas");
                canvastoadd.style.width = canvas.style.width;
                canvastoadd.style.height = canvas.style.height;
                canvastoadd.width = canvas.width;
                canvastoadd.height = canvas.height;
                canvastoadd.style.left = "0px";
                canvastoadd.style.top = "0px";
                canvastoadd.style.position = "absolute";
                canvastoadd.setAttribute("id", "canvas-" + canvas_index);
                document.getElementById("canvas").style.display='block';
                canvaslist.appendChild(canvastoadd);
                canvastodraw = canvastoadd;
                canvas_index++;
            }
            document.getElementById('addcanvas').onclick = addcanvas;
            /*canvas生成圆点*/
            function GetRandomNum(Min, Max) {
                var Range = Max - Min;
                var Rand = Math.random();
                return (Min + Math.round(Rand * Range));
            }
            function makearc(ctx, x, y, r, s, e, color) {
                ctx.clearRect(0, 0, ctx.width, ctx.height);//清空画布
                ctx.beginPath();
                ctx.fillStyle = color;
                ctx.arc(x, y, r, s, e);
                ctx.fill();
            }
            //video control
            playBtn.addEventListener('click', function(){
                if(playerTop.paused()){
                    // 如果视频处于播放状态
                    playerTop.play()
                    this.classList.remove('fa-play')
                    this.classList.add('fa-pause')
                }else{
                    playerTop.pause()
                    this.classList.add('fa-play')
                    this.classList.remove('fa-pause')
                }
            })
            innerbar.addEventListener('click', function(e){
                if(playerTop.paused() || playerTop.ended()){
                        playerTop.play()
                        playBtn.classList.remove('fa-play')
                        playBtn.classList.add('fa-pause')
                        enhanceVideoSeek(e);
                }
                else{
                        enhanceVideoSeek(e);
                }
            })
            function enhanceVideoSeek(e){
                var length = e.pageX - innerbar.offsetLeft-player.offsetLeft;
                var percent = length / innerbar.offsetWidth;
                progress.style.width = percent*innerbar.style.width+'px';
                playerTop.currentTime(percent * playerTop.duration());
                playerTop.play()
                playBtn.classList.remove('fa-play')
                playBtn.classList.add('fa-pause')
            }
            expand.addEventListener('click',function(){
                playerTop.toggleFullScreen();
            })
            Rect.init("main");
            //add rectangle button
            function cancelbutton() {
                Rect.container.onmousedown = null;
                document.getElementById('addrectangle').value="添加矩形";
                document.getElementById('addrectangle').onclick = beginbutton;
            }
            function beginbutton() {
                Rect.container.onmousedown = Rect.start;
                document.getElementById('addrectangle').value="取消添加矩形";
                document.getElementById('addrectangle').onclick = cancelbutton;
            }
            //start mark button
            function beginmark(){
                document.getElementById('startmark').value="终止标记";
                playerTop.pause();
                playBtn.classList.add('fa-play');
                playBtn.classList.remove('fa-pause');
                document.getElementById('addrectangle').onclick = beginbutton;
                document.getElementById('addrectangle').style.display = "block";
                document.getElementById('addcanvas').style.display = "block";
                document.getElementById('startmark').onclick = cancelmark;
                    
            }
            function cancelmark(){
                document.getElementById('startmark').value="开始标记";
                document.getElementById('addrectangle').style.display = "none";
                document.getElementById('addcanvas').style.display = "none";
                document.getElementById('startmark').onclick = beginmark;

            }
            document.getElementById('addrectangle').onclick = beginbutton;
            document.getElementById('startmark').onclick = beginmark;
    
            //upload mark button
            // var uploadbutton = document.getElementById("uploadbutton");
            var mb = document.getElementById('main');
            function draw_rec(board, name, left, top, height, width, transform){
                console.log("draw_rec");
                var r = document.createElement('div');
                let canvasindextop = parseInt(mb.offsetTop);
                let canvasindexleft = parseInt(mb.offsetLeft);
                r.style.position = "absolute"; 
                r.style.left = (parseInt(left)+canvasindexleft)+"px";
                r.style.top = (parseInt(top)+canvasindextop)+"px";
                r.style.height = height;
                r.style.width = width;
                r.style.border = "solid black 1px"; 
                r.style.transform = transform;
                var deleteLink = document.createElement('a'); 
                deleteLink.href="javascript:void(0);"; 
                deleteLink.onclick = function(){ 
                    Rect.container.removeChild(this.parentNode);  
                }
                deleteLink.innerText = "x";
                var givename = document.createElement('a');
                var showname = document.createElement('a');
                showname.innerText = name;
                givename.href = "javascript:void(0);";
                givename.onclick = function(){ 
                    ElMessageBox.prompt("请输入此区域名称", '输入任意非中文字符', {
                        confirmButtonText: '确认',
                        cancelButtonText: '取消',
                        inputValue: r.getAttribute("name")})
                    .then(({ value }) => {
                        //console.log(`input ${value}`)
                        r.setAttribute("name",value);
                        showname.innerText = value;
                    })
                    .catch(() => {
                        console.log('cancel input')
                    })
                }
                r.setAttribute("name",name);
                givename.innerText = "+";
                r.appendChild(deleteLink); 
                r.appendChild(givename); 
                r.appendChild(showname);
                r.setAttribute("class","rectangle");
                board.appendChild(r);
                r.onmousedown=rotatedown;
                r.onmousemove = rotatemove;
                r.onmouseup = rotateup;
            }
            function draw_poly(canvaslist,poly_info){
                var detail = poly_info.split(/[,;]/);
                var name = detail[0];
                var new_canvas = document.createElement('canvas');
                new_canvas.setAttribute("class", "ud_canvas");
                new_canvas.style.width = canvas.style.width;
                new_canvas.style.height = canvas.style.height;
                new_canvas.width = canvas.width;
                new_canvas.height = canvas.height;
                new_canvas.style.left = "0px";
                new_canvas.style.top = "0px";
                new_canvas.style.position = "absolute";
                new_canvas.setAttribute("id", "canvas-" + canvas_index);
                canvaslist.appendChild(new_canvas);
                var ctx = new_canvas.getContext('2d');
                ctx.beginPath();
                var sum_xindex = parseInt(detail[1]);
                var sum_yindex = parseInt(detail[2]);
                ctx.moveTo(detail[1],detail[2]);
                let canvasindextop = parseInt(mb.offsetTop);
                let canvasindexleft = parseInt(mb.offsetLeft);
                sum_xindex+=canvasindexleft;
                sum_yindex+=canvasindextop;
                let j = 0;
                for (j = 3; j<=detail.length-3; j=j+2){
                    sum_xindex+=parseInt(detail[j]);
                    sum_xindex+=canvasindexleft;
                    sum_yindex+=parseInt(detail[j+1]);
                    sum_yindex+=canvasindextop;
                    ctx.lineTo(detail[j],detail[j+1]); 
                }
                ctx.closePath();
                ctx.stroke();
                sum_xindex = sum_xindex/((detail.length-2)/2);
                sum_yindex = sum_yindex/((detail.length-2)/2);
                var givename = document.createElement('a');
                var showname = document.createElement('a');
                new_canvas.setAttribute("name",name);
                showname.innerText = name;
                givename.href = "javascript:void(0);";
                givename.onclick = function(){ 
                    ElMessageBox.prompt("请输入此区域名称", '输入任意非中文字符', {
                        confirmButtonText: '确认',
                        cancelButtonText: '取消',
                        inputValue: new_canvas.getAttribute("name")})
                    .then(({ value }) => {
                        //console.log(`input ${value}`)
                        new_canvas.setAttribute("name",value);
                        showname.innerText = value;
                    })
                    .catch(() => {
                        console.log('cancel input')
                    })
                } 
                givename.style.position="absolute";
                givename.style.top = sum_yindex+"px";
                givename.style.left = (sum_xindex+12)+"px";
                givename.innerText = "+";
                var deleteLink = document.createElement('a'); 
                deleteLink.href="javascript:void(0);"; 
                deleteLink.onclick = function(){ 
                    canvaslist.removeChild(new_canvas); 
                    this.remove();
                    givename.remove();
                    showname.remove();
                }
                deleteLink.style.position="absolute";
                deleteLink.style.top = sum_yindex+"px";
                deleteLink.style.left = sum_xindex+"px";
                deleteLink.innerText = "x";
                showname.style.position="absolute";
                showname.style.top = sum_yindex+17+"px";
                showname.style.left = sum_xindex+"px";
                board.appendChild(deleteLink);
                board.appendChild(givename);
                board.appendChild(showname);
                new_canvas.dataset.points = poly_info.substring((poly_info.indexOf(",")+1));
                canvas_index++;
                
            }
            var board = document.getElementById("main");
            // var canvaslist = document.getElementById("canvaslist");
            uploadbutton.addEventListener("change", (e) =>{
                var input = e.target;
                var reader = new FileReader();
                let i = 0;
                reader.onload = function() {
                    if(reader.result) {
                        //console.log(reader.result);
                        var input_data = reader.result.split('\n');
                        var rec_num = parseInt(input_data[0]);
                        //console.log(rec_num);
                        for (i=1; i<=rec_num; i++){
                            var rec_info = input_data[i].split(',');
                            draw_rec(board,rec_info[0],rec_info[1],rec_info[2],rec_info[3],rec_info[4],rec_info[5]);
                        }
                        var poly_num = parseInt(input_data[rec_num+1]);
                        //console.log(poly_num);
                        for (i=rec_num+2; i<rec_num+2+poly_num; i++){
                            draw_poly(canvaslist,input_data[i]);
                        }
                    }
                };
                reader.readAsText(input.files[0]);
                uploadbutton.value=null;
                    
            });
            //get result
            function runit(){
                // fileImport()
                console.log(__this.checkedParts)
                if (__this.checkedParts.length==0){
                    window.alert('请至少选择一个感兴趣的部位').then(() => {
                        console.log('ok');
                    });
                    //console.log("no select!!!!")
                    return;
                }
                console.log(__this.videopath)
                if (__this.videopath==""){
                    return;}
                let data =[]
                var father_board = document.getElementById('main');
                var all_rectangles = document.getElementsByClassName('rectangle');
                var all_ud_canvases = document.getElementsByClassName('ud_canvas');
                let csvString = "";
                const showedvideowidth = 800;
                const showedvideoheight = 450;
                data.push(showedvideowidth);
                data.push(showedvideoheight);
                data.push(all_rectangles.length);
                let topappend = parseInt(father_board.offsetTop);
                let leftappend = parseInt(father_board.offsetLeft);
                let i=0;
                for (i=0; i<all_rectangles.length; i++){
                        var child = all_rectangles[i];
                        let temp = "";
                        let leftindex = parseInt(child.style.left)-leftappend;
                        let topindex = parseInt(child.style.top)-topappend;
                        temp = temp + child.getAttribute('name') + "," + (leftindex+"px")+ "," +(topindex+"px")+"," +child.style.height+"," +child.style.width+","+child.style.transform;
                        //temp.push(child.getAttribute('name'),child.style.left,child.style.top,child.style.height,child.style.width,child.style.transform);
                        //console.log(temp);
                        data.push(temp);

                }
                data.push(all_ud_canvases.length);
                for (i=0; i<all_ud_canvases.length; i++){
                        var child = all_ud_canvases[i];
                        let temp = "";
                        temp = temp + child.getAttribute('name')+ ","+child.getAttribute('data-points')
                        //temp.push(child.getAttribute('name'),child.getAttribute('data-points'));
                        //console.log(temp);
                        data.push(temp);
                }
                console.log(data)
                console.log(__this.videoname)
                //console.log(that.videopath)
                data.push(__this.videopath)
                data.push(__this.videoname)
                data.push(__this.checkedParts)
                console.log(data)
                fetch('http://127.0.0.1:5001/api/runtrack', {
                    method: 'POST',
                    body: JSON.stringify({
                        argvs: data
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(response => {
                let result = response.text()
                result.then(res => {
                    console.log(res);
                    window.alert('通知', '处理完毕').then(() => {});
                })})

            }
            document.getElementById('rundetect').onclick = runit;
        },
        methods: {
            onRunit(){
                this.$refs.runItButton.click();
            },
            onUploadMark(){
                this.$refs.markInput.click();
            },
            onSelectVideo(){
                //console.log("1");
                this.$refs.videoInput.click();
            },
            selectvideo(){
                const files = event.target.files;
                console.log('files', files);
                let name = files[0].name;
                let dot_index = name.lastIndexOf('.');
                this.videoname = name.substring(0,dot_index);
                //console.log(this.videoname)
                this.videopath = files[0].path;
                //console.log(this.videopath)
                let url = URL.createObjectURL(files[0]);
                let vv = document.getElementById('video_id');
                vv.src=url;
            },
            savemark(){
                let i = 0;
                var all_rectangles = document.getElementsByClassName('rectangle');
                var all_ud_canvases = document.getElementsByClassName('ud_canvas');
                let canvasindextop = parseInt(this.$refs.mainboard.offsetTop);
                let canvasindexleft = parseInt(this.$refs.mainboard.offsetLeft);
                let data =[]
                data.push(all_rectangles.length+"\n");
                
                for (i=0; i<all_rectangles.length; i++){
                        var child = all_rectangles[i];
                        let temp = [];
                        temp.push(child.getAttribute('name'),(parseInt(child.style.left)-canvasindexleft)+"px",(parseInt(child.style.top)-canvasindextop)+"px",child.style.height,child.style.width,child.style.transform);
                        //console.log(temp);
                        data.push(temp+"\n");
                }
                data.push(all_ud_canvases.length+"\n");
                for (i=0; i<all_ud_canvases.length; i++){
                        var child = all_ud_canvases[i];
                        let temp = [];
                        temp.push(child.getAttribute('name'),child.getAttribute('data-points'));
                        //console.log(temp);
                        data.push(temp+"\n");
                }
                //console.log(data)
                const blob = new Blob(data , {type: "text/plain;charset=utf-8"})
                const objectURL = URL.createObjectURL(blob)
                //console.log(videoname);
                const link = document.createElement("a");
                link.download = this.videoname+".txt";
                console.log(this.videoname)
                link.style.display = 'none';
                link.href = URL.createObjectURL(blob); 
                link.click();
            },
            handleCheckAllChange(val) {
                this.checkedParts= val ? bodypartOptions: [];
                this.isIndeterminate = false; 
            },
            handleCheckedPartsChange(value) {
                let checkedCount = value.length;
                this.checkAll = checkedCount === this.partsArr.length;
                this.isIndeterminate = checkedCount > 0 && checkedCount < this.partsArr.length;
            },
            embyPot() {
                let resultvideopath = this.videopath+"/result/"+this.videoname+"_result.mp4";
                console.log(resultvideopath);
                let poturl = `potplayer://${resultvideopath}`;
                poturl = poturl.replaceAll("\\","\/");
                console.log(poturl);
                window.open(poturl, "_parent");
            },


        }

    }
    
</script>
<style lang="scss" scoped>
    #control_bar{
        left:auto;
        width: 800px;
    }
    #main{
        width:800px;
        height:450px;
    }
    canvas {
        border: 1px solid #333;
        display: block;
    }
    #canvas{
        width:800px;
        height:450px;
        position: absolute;
        left: 0;
        top: 0;
        z-index: 1;
        cursor: crosshair;
        display: none;
    }
    el-breadcrumb{
      padding-left: 40px;
      .el-breadcrumb__item{
          font-size: 15px;
          color: #606266 !important;
          font-weight: 500;
      }
      .el-breadcrumb__inner a, .el-breadcrumb__inner.is-link{
          color: #606266 !important;
          font-weight: 500;
      }
    }
</style>