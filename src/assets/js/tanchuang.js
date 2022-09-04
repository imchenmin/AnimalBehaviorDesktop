// 获取弹窗
var modal = document.getElementById('myModal');
mouse_index = 0;
// 获取图片插入到弹窗 - 使用 "alt" 属性作为文本部分的内容
var img = document.getElementById('test_tan');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var span = document.getElementById("closemodal");
var redo = document.getElementById("redomodal");
modalImg.onclick = function (e) {
  var e1 = e || window.event;
  var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
  var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
  var x = e1.pageX || e1.clientX + scrollX;
  var y = e1.pageY || e1.clientY + scrollY;
  console.log(x)
  console.log(y)
  var index = document.createElement('a');
  index.className = "index_label";
  index.innerText = mouse_index;
  mouse_index = mouse_index + 1;
  index.style.left = x;
  index.style.top = y;
  index.style.position = "absolute"
  modal.appendChild(index);
}
img.onclick = function () {
  console.log("11111111");
  modalImg.src="static/temp_photo.png?t" + Math.random();
  modal.style.display = "block";
  captionText.innerHTML = "testtest";
  modal.style.width = modalImg.src.width + "px";
  modal.style.height = modalImg.src.width + "px";
  modalImg.style.width = modalImg.src.width + "px";
  modalImg.style.height = modalImg.src.height + "px";
  // span.style.top = modalImg.src.height + "px";
  // redo.style.top = modalImg.src.height + "px";

}


span.onclick = function () {
  modal.style.display = "none";
  var labels = document.getElementsByClassName("index_label");
  var index_labels =[];

  if (labels.length != undefined) {
    for (var i = labels.length - 1; i >= 0; i--) {
      // index_labels.push(labels[i].style.width);
      // index_labels.push(labels[i].style.height);
      index_labels.push(parseInt(labels[i].style.left)-8);  //左边8的bias
      index_labels.push(parseInt(labels[i].style.top)-50); //上面50的bias
      labels[i].remove();
      console.log(i);
    }
  }
  
  console.log(index_labels);

  mouse_index = 0;
  if(windw_socket!=null){
    windw_socket.emit('selectIndex', index_labels);
  }
}
redo.onclick = function () {
  var labels = document.getElementsByClassName("index_label");
  if (labels.length != undefined) {
    for (var i = labels.length - 1; i >= 0; i--) {
      labels[i].remove();
      console.log(i);
    }
  }
  mouse_index = 0;
  
}