const ipc = require('electron').ipcRenderer
//
// const syncMsgBtn = document.getElementById('sync-msg')
//
// clearItem()
//
// syncMsgBtn.addEventListener('click', function() {
//
//   // const message = `Synchronous message reply: ${reply}`
//   // document.getElementById('sync-reply').innerHTML = message
//   var reply = ipc.sendSync('synchronous-message', 'get item')
//   while (true) {
//     console.log(reply)
//     if (reply == "nomore") {
//       break
//     }
//     var newItem = reply.split(" ")
//     addItem(newItem)
//     var reply = ipc.sendSync('synchronous-message', 'anymore')
//   }
// })
clearItem()
const asyncMsgBtn = document.getElementById('async-msg')

asyncMsgBtn.addEventListener('click', function() {
  ipc.send('asynchronous-message', 'get item')
})

ipc.on('asynchronous-reply', function(event, arg) {
  if (arg != "nomore") {
    var newItem = arg.slice(2, arg.length - 2).split("\", \"")
    // var newNewItem = unescape(encodeURIComponent(newItem[0]))
    var newNewItem = unescape(decodeURIComponent(newItem[0]))
    console.log(newNewItem)
    console.log("")
    addItem(newItem)
    ipc.send('asynchronous-message', 'anymore')
  }
})

function addNav(newNav) {

}

function clearNav() {

}

function changeTitle(newTitle) {

}

function change2ndTitle(newTitle) {

}

function addItem(newItem) {
  var new_tr = document.createElement("tr")
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode("1,000")
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  var num = document.createElement("td")
  var node = document.createTextNode("1,000")
  num.appendChild(node)
  new_tr.appendChild(num)
  var num = document.createElement("td")
  var node = document.createTextNode("1,000")
  num.appendChild(node)
  new_tr.appendChild(num)
  var num = document.createElement("td")
  var node = document.createTextNode("1,000")
  num.appendChild(node)
  new_tr.appendChild(num)
  var num = document.createElement("td")
  var node = document.createTextNode("1,000")
  num.appendChild(node)
  new_tr.appendChild(num)
  var test = document.getElementById("test")
  test.appendChild(new_tr)
}

function clearItem() {

}
