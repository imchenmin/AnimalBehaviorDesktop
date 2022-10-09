const interfaces = require('os').networkInterfaces(); //服务器本机地址
let IPAdress = '';
for (var devName in interfaces) {
    var iface = interfaces[devName];
    console.log(iface)
    for (var i = 0; i < iface.length; i++) {
        var alias = iface[i];
        if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
            IPAdress = alias.address;
        }
    }
} 