$('#camera_switch').change(function () {
    let cam_switch = $('#camera_switch').prop("checked");
    if (cam_switch){
        connect('origin_cam')
    }
    else{
        if (last_socket){
            last_socket.close()
        }
        $('#target').attr('src', '/static/plugin/img/cam.jpg')
    }
});
$('#face_switch').change(function () {
    let cam_switch = $('#face_switch').prop("checked");
    if (cam_switch){
        connect('face_cam')
    }
    else{
        if (last_socket){
            last_socket.close()
        }
        $('#target').attr('src', '/static/plugin/img/cam.jpg')
    }
});

// function connect(){
//     let socket = new WebSocket("ws://"+window.location.host+"/ws/queue/");
//     socket.onopen = function (evt) {
//         socket.send('face_cam');
//         console.log('客户端成功建立连接。。')
//     };
//
//     socket.onmessage = function (evt) {
//         let blob = evt.data;
//         let reader = new FileReader();
//
//         reader.readAsDataURL(blob);
//         reader.onload = function(e) {
//             let img = document.getElementById("target");
//             img.src = this.result;
//
//         }
//     };
//     socket.onclose = function() {
//         console.log("Closed");
//         socket.close()
//     };
//
//     socket.onerror = function(err) {
//         console.log("Error: " + err);
//     };
// }




