$(function () {
    $('.btn').attr('disabled',true);
    $('#target').attr('src', '/static/plugin/img/cam.jpg')
});
$('#car_switch').change(function () {
    let swit = $('#car_switch').prop("checked")
    if (swit){
        $('.btn').attr('disabled',false)
    }
    else {
        $('.btn').attr('disabled',true);
    }
});

$('.btn').click(function () {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.dataCommand,
        data : {'command':this.value},
        success : function(data) {
            if (data.ret){
            }
            else{
                console.log(data.msg)
            }
        },
        error : function(e){
            console.log(e.status);
            console.log(e.responseText);
        }
    });
    console.log(this.value)
});

$('#camera_switch').change(function () {
    let cam_switch = $('#camera_switch').prop("checked");
    if (cam_switch){
        connect('origin')
    }
    else{
        if (last_socket){
            last_socket.close()
        }
        $('#target').attr('src', '../static/plugin/img/cam.jpg')
    }
});

// function connect(){
//     let socket = new WebSocket("ws://"+window.location.host+"/ws/queue/");
//     socket.onopen = function (evt) {
//         socket.send('origin_cam');
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