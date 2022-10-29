// 使用socketio和express作为状态的测试服务器，用来调试前端代码
const http = require('http');
const path = require('path');
const express = require('express');
//创建一个应用，注意app其实就是一个函数，类似function(req, res) {}
let app = express();
//创建一个http服务器，既然app是一个函数，那这里就可以传入。
let server = http.createServer(app);
//注意，websocket的握手是需要依赖http服务的，所以这里要把server传入进去。
let io = require('socket.io')(server);
 
app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'socket_index.html'));
});

class ProcessingObject {
    constructor(project_path,ptype) {
        this.ptype = ptype
        // this.project_id = project_id
        this.project_path = project_path
        this.progress = 0.0
        this.status = 0

    }
}
//有新的客户端连接时触发
io.on('connection', function (socket) {
    //接收到消息时触发
    socket.on('message', function (data) {
        console.log('服务端收到 : ', data);
        //注意send()方法其实是发送一个 'message' 事件
        //客户端要通过on('message')来响应
        socket.send('你好客户端, ' + data);
    });
    socket.on('require_project_status',(data)=>{
        console.log(data)
        let list = data.project_list
        let progressList = []
        for (let i = 0; i < list.length; i++) {
            progressList.push(new ProcessingObject(list[i],1))
        }
        var timer = setInterval(()=>{ 
            for (let i = 0; i < progressList.length; i++) {
                progressList[i].progress += 10
            }

            socket.emit('project_status',{
                msg: progressList,
                code: 200
            })        
            if (progressList[0].progress >= 100) {
                clearInterval(timer)
            }
        }, 1000); 
    })
    //发生错误时触发
    socket.on('error', function (err) {
        console.log(err);
    });
});
 
server.listen(8867);