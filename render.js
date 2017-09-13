const ipc = require('electron').ipcRenderer
clearItem()
const asyncMsgBtn = document.getElementById('async-msg')

asyncMsgBtn.addEventListener('click', function() {
  ipc.send('asynchronous-message', 'get item')
})

ipc.on('asynchronous-reply', function(event, arg) {
  if (arg != "nomore") {
    var newItem = arg.slice(2, arg.length - 2).split("\", \"")
    var newNewItem = unescape(decodeURIComponent(newItem[0]))
    console.log(newNewItem)
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
  // 代码
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[0])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 名称
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[1])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 当前
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[2])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 今开
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[3])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 昨收
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[4])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 最高
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[5])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 最低
  var new_td = document.createElement("td")
  var new_textnode = document.createTextNode(newItem[6])
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  // 操作
  var new_td = document.createElement("button")
  new_td.type = "button"
  new_td.className = "btn btn-primary"
  var new_textnode = document.createTextNode("买入")
  new_td.appendChild(new_textnode)
  new_tr.appendChild(new_td)
  new_td.setAttribute("id", newItem[0])
  new_td.addEventListener("click", function() {
    alert(this.id);
  })

  var test = document.getElementById("test")
  test.appendChild(new_tr)
}

function clearItem() {
  var test = document.getElementById("test")
  while (test.hasChildNodes()) //当div下还存在子节点时 循环继续
  {
    test.removeChild(test.firstChild);
  }

}
