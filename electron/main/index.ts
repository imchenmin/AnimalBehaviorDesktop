import { app, BrowserWindow, shell, ipcMain, dialog } from 'electron'
import { release } from 'os'
import { join } from 'path'

import { videoSupport } from './ffmpeg-helper';
import VideoServer from './VideoServer';
import CameraServer from './CameraServer'

//--- add native video part
let httpServer;
let isRendererReady = false;
let win: BrowserWindow | null = null
// Here, you can also use other preload
function onTopCameraStarted() {

}
function onCameraRecording(saveVideoPathTop='', saveVideoPathSide='') {
      if (!httpServer) {
          httpServer = new CameraServer({_side:true,_top:true});
      }
      httpServer.saveVideoPath = { saveVideoPathTop: saveVideoPathTop, saveVideoPathSide: saveVideoPathSide };
      httpServer.createCameraServer();
      console.log("createVideoServer success",httpServer);
      let playParams = {type:'stream', videoSourceTop:"http://127.0.0.1:8889",videoSourceSide:"http://127.0.0.1:8890"}
      console.log("cameraRecoridng=", playParams)

      win.webContents.send('cameraRecoridng', playParams)
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
  ipcMain.on('cameraRecording', function (event, arg) {
    console.log("cameraRecording:", arg);
    onCameraRecording(arg);
  });
  ipcMain.on('stopRecord', function(event,arg) {
    console.log('stopRecord', arg)
    if (!httpServer) {
      console.log("HTTPServer didn't exist, so ignore stop command")
      return
    }
    httpServer.stopFFmpegCommand()
  })
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
