$(function () {
    $('#target').attr('src', '/static/plugin/img/cam.jpg')
});
$('#btn_connect').click(function () {
    $('#btn_connect').addClass('loading');
    $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.connectDevice,
        data : {'command':this.value},
        success : function(data) {
            if (data.ret){
                let device = $('#device_state');
                device.removeClass('red');
                device.removeClass('green');
                device.empty();
                device.append('<i class="rss green icon"></i>\n' +
                    '                    当前设备在线');
                alert('连接成功');
            }
            else{
                alert('连接失败');
                console.log(data.msg)
            }
            $('#btn_connect').removeClass('loading');
        },
        error : function(e){
            console.log(e.status);
            console.log(e.responseText);
        }
    });
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