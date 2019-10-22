$('.cam').click(function () {
    let type = this.value;
    if (last_socket){
        last_socket.close()
    }
    if (type=== 'close'){
        $('#target').attr('src', '../static/plugin/img/cam1.jpg')
        close_client()
    }else{
        connect(type)
    }
});


