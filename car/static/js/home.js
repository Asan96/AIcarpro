let last_socket;
let device_state = $('#device_state').val();
if (device_state ==='online'){
    $('#device_state_online').show();
    $('#device_state_outline').hide();
}else{
    $('#device_state_online').hide();
    $('#device_state_outline').show();
}
function connect(command){
    console.log(last_socket);
    if (last_socket){
        last_socket.close()
    }
    let socket = new WebSocket("ws://"+window.location.host+"/ws/queue/");
    last_socket = socket;
    socket.onopen = function (evt) {
        socket.send(command);
        console.log('客户端成功建立连接。。');
        $('#target').attr('src', '/static/plugin/img/loading.gif')
    };

    socket.onmessage = function (evt) {
        let blob = evt.data;
        let reader = new FileReader();

        reader.readAsDataURL(blob);
        reader.onload = function(e) {
            let img = document.getElementById("target");
            img.src = this.result;

        }
    };
    socket.onclose = function() {
        socket.close()
    };

    socket.onerror = function(err) {
        console.log("Error: " + err);
    };
}