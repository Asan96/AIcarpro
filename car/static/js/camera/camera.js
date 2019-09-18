$('.cam').click(function () {
    let type = this.value;
    if (last_socket){
        last_socket.close()
    }
    if (type=== 'close'){
        $('#target').attr('src', '../static/plugin/img/cam1.jpg')
    }else{
        connect(type)
    }
});


