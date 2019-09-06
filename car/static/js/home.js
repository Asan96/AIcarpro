let last_socket;
function connect(command){
    if (last_socket){
        last_socket.close()
    }
    let socket = new WebSocket("ws://"+window.location.host+"/ws/queue/");
    last_socket = socket;
    socket.onopen = function (evt) {
        socket.send(command);
        console.log('客户端成功建立连接。。')
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
        console.log("Closed");
        socket.close()
    };

    socket.onerror = function(err) {
        console.log("Error: " + err);
    };
}