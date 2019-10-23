$(function () {
    $('#target').attr('src', '/static/plugin/img/cam.jpg')
});
$('#btn_connect').click(function () {
    $('#btn_connect').addClass('loading');
    let device_id = $('#device_id').val();
    if (!isNaN(device_id)){
        $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.connectMqtt,
        data : {'device_id':device_id},
        success : function(data) {
            if (data.ret){
                $('#device_state_online').show();
                $('#device_state_outline').hide();
                $('#device_state_online').empty();
                $('#device_state_online').empty();
                $('#device_state_online').append('<h4 style="color: green"><i class="rss green icon"></i>设备建立连接 设备号： '+device_id+ '</h4>');
                alert('建立连接成功!设备号'+device_id);
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
    }
    else{
        alert('请输入正确的设备编号!')
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
        close_client()
        $('#target').attr('src', '../static/plugin/img/cam.jpg')
    }
});
$('#wifi_settings').click(function () {
    $('.ui.modal').modal('show');
    $('#set_wifi').unbind().click(function () {
        let wifi_name = $('#wifi_name').val();
        let wifi_pwd = $('#wifi_pwd').val();
        $.ajax({
            type : "POST",
            dataType: "json",
            url : PUB_URL.setWifi,
            data : {'wifi_name':wifi_name,'wifi_pwd':wifi_pwd},
            success : function(data) {
                if (data.ret){
                    $('.ui.modal').modal('hide');
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
    })
    $('.wifi').val('');
});