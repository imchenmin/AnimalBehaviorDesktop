import { app, BrowserWindow, shell, ipcMain, dialog } from "electron";
import { release } from "os";
import { join } from "path";
const { spawn, exec } = require("child_process");


import { videoSupport } from "./ffmpeg-helper";
import VideoServer from "./VideoServer";
//--- add native video part
let videoServer;
let isRendererReady = false;
let win: BrowserWindow | null = null;
// Here, you can also use other preload
const fork = require("child_process").fork;
app.disableHardwareAcceleration()

const Stream = require('node-rtsp-stream')
/**
 * rtsp列表
 * interface {
 *   rtspUrl: {
 *     ws: websocket地址
 *     stream: stream实例
 *   }
 * }
 */
const rtspOpenders = {}
let addPort = 9000
const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;
var express = require("express");
var expressWebSocket = require("express-ws");
const ffmpeg = require('fluent-ffmpeg');
ffmpeg.setFfmpegPath(ffmpegPath);
var webSocketStream = require("websocket-stream/stream");
var WebSocket = require("websocket-stream");
var http = require("http");
function localServer() {
  let app = express();
  app.use(express.static(__dirname));
  expressWebSocket(app, null, {
    perMessageDeflate: true
  });
  app.ws("/rtsp/:id/", rtspRequestHandle)
  app.listen(8899);
  console.log("express listened")
}
function rtspRequestHandle(ws, req) {
  console.log("rtsp request handle");
  const stream = webSocketStream(ws, {
    binary: true,
    browserBufferTimeout: 1000000
  }, {
    browserBufferTimeout: 1000000
  });
  let url = req.query.url;
  console.log("rtsp url:", url);
  console.log("rtsp params:", req.params);
  try {
    ffmpeg(url)
      .addInputOption("-rtsp_transport", "tcp", "-buffer_size", "102400")  // 这里可以添加一些 RTSP 优化的参数
      .on("start", function () {
        console.log(url, "Stream started.");
      })
      .on("codecData", function () {
        console.log(url, "Stream codecData.")
        // 摄像机在线处理
      })
      .on("error", function (err) {
        console.log(url, "An error occured: ", err.message);
      })
      .on("end", function () {
        console.log(url, "Stream end!");
        // 摄像机断线的处理
      })
      .outputFormat("flv").videoCodec("copy").noAudio().pipe(stream);
  } catch (error) {
    console.log(error);
  }
}
function onVideoFileSeleted(videoFilePath) {
  videoSupport(videoFilePath)
    .then((checkResult) => {
      console.log(checkResult);
      
      if (checkResult.videoCodecSupport) {
        if (!videoServer) {
          videoServer = new VideoServer();
        } else {
          videoServer.killFfmpegCommand();
          videoServer = new VideoServer();
        }
        videoServer.videoSourceInfo = {
          videoSourcePath: videoFilePath,
          checkResult: checkResult,
        };
        videoServer.createServer();
        console.log("createVideoServer success");
        let playParams = { type: "", videoSource: "", duration: 0 };
        playParams.type = "stream";
        playParams.videoSource = "http://127.0.0.1:8888?startTime=0";
        playParams.duration = checkResult.duration;
        console.log("videoServerReady=", playParams);
        win.webContents.send("videoServerReady", playParams);
      }
    })
    .catch((err) => {
      console.log("video format error", err);
      dialog.showMessageBox({
        title: "错误信息",
        type: "info",
        message: "It is not a video file!",
        buttons: ["OK"]
      });
    });
}
// Disable GPU Acceleration for Windows 7
if (release().startsWith("6.1")) app.disableHardwareAcceleration();

// Set application name for Windows 10+ notifications
if (process.platform === "win32") app.setAppUserModelId(app.getName());

if (!app.requestSingleInstanceLock()) {
  app.quit();
  process.exit(0);
}

// Remove electron security warnings
// This warning only shows in development mode
// Read more on https://www.electronjs.org/docs/latest/tutorial/security
// process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true'

export const ROOT_PATH = {
  // /dist
  dist: join(__dirname, "../.."),
  // /dist or /public
  public: join(__dirname, app.isPackaged ? "../.." : "../../../public"),
};

const { autoUpdater } = require("electron-updater");
function checkUpdate() {
  //检测更新
  autoUpdater.checkForUpdates();
  autoUpdater.on("check-for-update", (err) => {
    console.log(err);
  });
  console.log("checkupdate");
  //监听'error'事件
  autoUpdater.on("error", (err) => {
    console.log(err);
  });

  //监听'update-available'事件，发现有新版本时触发
  autoUpdater.on("update-available", () => {
    console.log("found new version");
  });

  //默认会自动下载新版本，如果不想自动下载，设置autoUpdater.autoDownload = false

  //监听'update-downloaded'事件，新版本下载完成时触发
  autoUpdater.on("update-downloaded", () => {
    dialog
      .showMessageBox({
        type: "info",
        title: "应用更新",
        message: "发现新版本，是否更新？",
        buttons: ["是", "否"],
      })
      .then((buttonIndex) => {
        if (buttonIndex.response == 0) {
          //选择是，则退出程序，安装新版本
          autoUpdater.quitAndInstall();
          app.quit();
        }
      });
  });
}
// new window example arg: new windows url
ipcMain.handle("open-win", (event, arg) => {
  const childWindow = new BrowserWindow({
    webPreferences: {
      preload,
    },
  });

  if (app.isPackaged) {
    childWindow.loadFile(indexHtml, { hash: arg });
  } else {
    childWindow.loadURL(`${url}/#${arg}`);
  }
});

const preload = join(__dirname, "../preload/index.js");
const url = "http://127.0.0.1:3000";
const indexHtml = join(ROOT_PATH.dist, "index.html");

async function createWindow() {
  const remote = require("@electron/remote/main");
  const { session } = require("electron");
  const path = require("path");
  win = new BrowserWindow({
    title: "Main window",
    icon: join(ROOT_PATH.public, "favicon.ico"),
    webPreferences: {
      preload,
      // Warning: Enable nodeIntegration and disable contextIsolation is not secure in production
      // Consider using contextBridge.exposeInMainWorld
      // Read more on https://www.electronjs.org/docs/latest/tutorial/context-isolation
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false,
    },
  });
  remote.initialize();
  remote.enable(win.webContents);
  if (app.isPackaged) {
    win.loadFile(indexHtml);
  } else {
    win.loadURL(url);
    // Open devTool if the app is not packaged
    // win.webContents.openDevTools()
    //TODO: 添加环境检测
    // let uri = path.resolve("./electron/6.2.1_0");
    // try {
    // await session.defaultSession.loadExtension(uri, { allowFileAccess: true });
    // }
    // catch (e) {
    //   console.log("error",e)
    // }
  }

  // Test actively push message to the Electron-Renderer
  win.webContents.on("did-finish-load", () => {
    win?.webContents.send("main-process-message", new Date().toLocaleString());
  });

  // Make all links open with the browser, not with the application
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("https:")) shell.openExternal(url);
    return { action: "deny" };
  });
  ipcMain.on("playVideoFromFile", function (event, arg1, arg2) {
    console.log("playVideoFromFile", arg1, arg2);
    onVideoFileSeleted(arg1); //目前只处理一个视频。
  });
  checkUpdate();
  localServer();
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  win = null;
  if (process.platform !== "darwin") app.quit();
});

app.on("second-instance", () => {
  if (win) {
    // Focus on the main window if the user tried to open another
    if (win.isMinimized()) win.restore();
    win.focus();
  }
});

app.on("activate", () => {
  const allWindows = BrowserWindow.getAllWindows();
  if (allWindows.length) {
    allWindows[0].focus();
  } else {
    createWindow();
  }
});

app.commandLine.appendSwitch("autoplay-policy", "no-user-gesture-required");
