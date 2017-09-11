const ipc = require('electron').ipcRenderer

const syncMsgBtn = document.getElementById('sync-msg')

syncMsgBtn.addEventListener('click', function() {
  const reply = ipc.sendSync('synchronous-message', 'ping')
  // const message = `Synchronous message reply: ${reply}`
  // document.getElementById('sync-reply').innerHTML = message

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
