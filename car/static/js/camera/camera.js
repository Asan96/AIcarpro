$('.cam_switch').change(function () {
    let type = this.value;
    let cam_switch = $('#'+type).prop("checked");
    if (cam_switch){
        connect(type)
    }
    else{
        if (last_socket){
            last_socket.close()
        }
        $('#target').attr('src', '/static/plugin/img/cam.jpg')
    }
});





