$('#open_camera').click(
    function () {
        $('#open_camera').hide()
        $('#close_camera').show()
        connect()
    }
);
$("#close_camera").click(function () {
    $('#open_camera').show();
    $('#close_camera').hide();
    $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.dataCloseServer,
        data : {},
        success : function(data) {
            if (data.ret){
                console.log(data.msg)
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

function connect(){
    let socket = new WebSocket("ws://"+window.location.host+"/ws/queue/");

    socket.onopen = function (evt) {
        socket.send('connected');
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




