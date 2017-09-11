const {
  app,
  Menu,
  BrowserWindow
} = require('electron')
const path = require('path')
const url = require('url')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win

// var ppp = require('child_process').spawn('DebugNext.bat')

const template = [{
    label: '游戏',
    submenu: [{
        label: '开始新游戏'
      },
      {
        type: 'separator'
      },
      {
        label: '注销账号'
      },
      {
        type: 'separator'
      },
      {
        label: '退出游戏'
      }
    ]
  },
  {
    label: '动作',
    submenu: [{
      label: '刷新数据'
    }]
  },
  {
    label: '视图',
  },
  {
    label: '工具',
    submenu: [{
        type: 'separator'
      },
      {
        label: '游戏设置'
      }
    ]
  },
  {
    label: '帮助',
    submenu: [{
        label: '文档'
      },
      {
        type: 'separator'
      },
      {
        label: '教程'
      },
      {
        type: 'separator'
      },
      {
        label: '更新'
      },
      {
        type: 'separator'
      },
      {
        label: '关于'
      }
    ]
  }
]
const menu = Menu.buildFromTemplate(template)
// Menu.setApplicationMenu(menu)
Menu.setApplicationMenu(menu)

var net = require('net');
var HOST = '127.0.0.1';
var PORT = 6969;
var client = new net.Socket();
client.bufferSize = 8000
client.connect(PORT, HOST, function() {
  console.log('CONNECTED TO: ' + HOST + ':' + PORT);
  // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client
  client.write('I am Chuck Norris!');
});
client.on('data', function(data) {
  console.log('DATA: ' + data);
  // Close the client socket completely
  client.destroy();
});
// Add a 'close' event handler for the client socket
client.on('close', function() {
  console.log('Connection closed');
});
client.on('error', function() {
  console.log('Connection error');
});


function createWindow() {
  // Create the browser window.
  win = new BrowserWindow({
    width: 1600,
    height: 900
  })
  win.setMenu(menu)
  // and load the index.html of the app.
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  // Open the DevTools.
  win.webContents.openDevTools()

  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
