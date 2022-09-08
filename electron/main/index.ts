import { app, BrowserWindow, shell, ipcMain, dialog } from 'electron'
import { release } from 'os'
import { join } from 'path'

import { videoSupport } from './ffmpeg-helper';
import VideoServer from './VideoServer';

//--- add native video part
let httpServer;
let isRendererReady = false;
let win: BrowserWindow | null = null
// Here, you can also use other preload

function onVideoFileSeleted(videoFilePath) {
  videoSupport(videoFilePath).then((checkResult) => {
      if (checkResult.videoCodecSupport && checkResult.audioCodecSupport) {
          if (httpServer) {
              httpServer.killFfmpegCommand();
          }
          let playParams = {type:'', videoSource:''};
          playParams.type = "native";
          playParams.videoSource = videoFilePath;
          if (isRendererReady) {
              console.log("fileSelected=", playParams)

              win.webContents.send('fileSelected', playParams);
          } else {
              ipcMain.once("ipcRendererReady", (event, args) => {
                  console.log("fileSelected", playParams)
                  win.webContents.send('fileSelected', playParams);
                  isRendererReady = true;
              })
          }
      }
      if (!checkResult.videoCodecSupport || !checkResult.audioCodecSupport) {
          if (!httpServer) {
              httpServer = new VideoServer();
          }
          httpServer.videoSourceInfo = { videoSourcePath: videoFilePath, checkResult: checkResult };
          httpServer.createServer();
          console.log("createVideoServer success");
          let playParams = {type:'', videoSource:'',duration: 0};
          playParams.type = "stream";
          playParams.videoSource = "http://127.0.0.1:8888?startTime=0";
          playParams.duration = checkResult.duration
          if (isRendererReady) {
              console.log("fileSelected=", playParams)

              win.webContents.send('fileSelected', playParams);
          } else {
              ipcMain.once("ipcRendererReady", (event, args) => {
                  console.log("fileSelected", playParams)
                  win.webContents.send('fileSelected', playParams);
                  isRendererReady = true;
              })
          }
      }
  }).catch((err) => {
      console.log("video format error", err);
      const options = {
          type: 'info',
          title: 'Error',
          message: "It is not a video file!",
          buttons: ['OK']
      }
  })
}
// Disable GPU Acceleration for Windows 7
if (release().startsWith('6.1')) app.disableHardwareAcceleration()

// Set application name for Windows 10+ notifications
if (process.platform === 'win32') app.setAppUserModelId(app.getName())

if (!app.requestSingleInstanceLock()) {
  app.quit()
  process.exit(0)
}

// Remove electron security warnings
// This warning only shows in development mode
// Read more on https://www.electronjs.org/docs/latest/tutorial/security
// process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true'

export const ROOT_PATH = {
  // /dist
  dist: join(__dirname, '../..'),
  // /dist or /public
  public: join(__dirname, app.isPackaged ? '../..' : '../../../public'),
}


const preload = join(__dirname, '../preload/index.js')
const url = "http://127.0.0.1:3000"
const indexHtml = join(ROOT_PATH.dist, 'index.html')

async function createWindow() {
  const remote = require('@electron/remote/main')
  win = new BrowserWindow({
    title: 'Main window',
    icon: join(ROOT_PATH.public, 'favicon.ico'),
    webPreferences: {
      preload,
      // Warning: Enable nodeIntegration and disable contextIsolation is not secure in production
      // Consider using contextBridge.exposeInMainWorld
      // Read more on https://www.electronjs.org/docs/latest/tutorial/context-isolation
      nodeIntegration: true,
      contextIsolation: false,
    },
  },
  )
  remote.initialize()
  remote.enable(win.webContents)
  if (app.isPackaged) {
    win.loadFile(indexHtml)
  } else {
    win.loadURL(url)
    // Open devTool if the app is not packaged
    // win.webContents.openDevTools()
  }

  // Test actively push message to the Electron-Renderer
  win.webContents.on('did-finish-load', () => {
    win?.webContents.send('main-process-message', new Date().toLocaleString())
  })

  // Make all links open with the browser, not with the application
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('https:')) shell.openExternal(url)
    return { action: 'deny' }
  })
  ipcMain.on('fileDrop', function (event, arg) {
    console.log("fileDrop:", arg);
    onVideoFileSeleted(arg);
  });
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  win = null
  if (process.platform !== 'darwin') app.quit()
})

app.on('second-instance', () => {
  if (win) {
    // Focus on the main window if the user tried to open another
    if (win.isMinimized()) win.restore()
    win.focus()
  }
})

app.on('activate', () => {
  const allWindows = BrowserWindow.getAllWindows()
  if (allWindows.length) {
    allWindows[0].focus()
  } else {
    createWindow()
  }
})

// new window example arg: new windows url
ipcMain.handle('open-win', (event, arg) => {
  const childWindow = new BrowserWindow({
    webPreferences: {
      preload,
    },
  })

  if (app.isPackaged) {
    childWindow.loadFile(indexHtml, { hash: arg })
  } else {
    childWindow.loadURL(`${url}/#${arg}`)
  }
})

app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
