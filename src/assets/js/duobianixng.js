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
        for (var i = 0; i<pointArr.length-1; i++){
            str = str+pointArr[i].x+","+pointArr[i].y+";";
            xindex+=pointArr[i].x;
            yindex+=pointArr[i].y;
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
    $('#addcanvas').click(function () {
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

    });

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