let key = 0;
$(function () {
    $('#target').attr('src', '/static/plugin/img/cam.jpg');
    //页面键盘点击时触发
    $(window).keydown(function(e){
        let curKey = e.which;
        let keyDic = { 65: 'car_right', 87 :'car_forward', 68:'car_left',83:'car_backward', 69:'car_stop',81:'car_rotate'};
        if(keyDic.hasOwnProperty(curKey) && key){
            console.log(keyDic[curKey]);
            mqtt_send(keyDic[curKey]);
        }
    })
});
$('#keyboard_switch').change(function () {
    let keyboard_switch = $('#keyboard_switch').prop("checked");
    console.log(keyboard_switch);
    if(keyboard_switch){
        key = 1;
    }else{
        key = 0;
        mqtt_send('car_stop');
    }
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
                let online = $('#device_state_online');
                online.show();
                $('#device_state_outline').hide();
                online.empty();
                online.append('<h4 style="color: green"><i class="rss green icon"></i>设备建立连接 设备号： '+device_id+ '</h4>');
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
    console.log(this.value);
    mqtt_send(this.value);
});

$('#avoid_switch').change(function () {
    let avoid_switch = $('#avoid_switch').prop("checked");
    let avoid_cmd;
    if (avoid_switch){
        avoid_cmd = 'avoid_on'
    }else{
        avoid_cmd = 'avoid_off'
    }
    mqtt_send(avoid_cmd);

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
        close_client();
        $('#target').attr('src', '../static/plugin/img/cam.jpg')
    }
});
$('#travel_switch').change(function () {
    let travel_switch = $('#travel_switch').prop("checked");
    let travel_cmd;
    if (travel_switch){
        travel_cmd = 'travel_on'
    }else{
        travel_cmd = 'travel_off'
    }
    mqtt_send(travel_cmd);
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
    });
    $('.wifi').val('');
});