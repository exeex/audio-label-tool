'use strict'

import {app, BrowserWindow} from 'electron'

const {ipcMain} = require('electron')
let PythonShell = require('python-shell').PythonShell
/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow

let opt = {
  mode: 'json',
  pythonOptions: ['-u'],
  pythonPath: 'python',
  scriptPath: './',
  encoding: 'utf8'
}

const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 563,
    useContentSize: true,
    width: 1000
  })

  mainWindow.loadURL(winURL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })

  ipcMain.on('index-page-ready', (event, status) => {
    let pyshell = new PythonShell('lyric.py', opt)
    pyshell.on('message', function (message) {
      mainWindow.webContents.send('load-lyric-done', message)
      console.log('haha')
    })
    pyshell.end()
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
