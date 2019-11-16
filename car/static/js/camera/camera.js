$('.cam').click(function () {
    let type = this.value;
    if (last_socket){
        last_socket.close()
    }
    if (type=== 'close'){
        $('#target').attr('src', '../static/plugin/img/cam1.jpg');
        close_client()
    }else{
        connect(type)
    }
});
/**
 * 拍照
 * */
$('.operate').click(function () {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.takePhoto,
        data : {},
        success : function(data) {
            if (data.ret){
            }
            else{
                alert(data.msg)
            }
        },
        error : function(e){
            console.log(e.status);
            console.log(e.responseText);
        }
    });
});



