/**
 * 文字对话
 * */
$('#send').click(function () {
    let myDate = new Date;
    let year = myDate.getFullYear(); //获取当前年
    let mon = myDate.getMonth() + 1; //获取当前月
    let date = myDate.getDate(); //获取当前日
    let h = myDate.getHours();//获取当前小时数(0-23)
    let m = myDate.getMinutes();//获取当前分钟数(0-59)
    let s = myDate.getSeconds();//获取当前秒
    let word = $('#word').val();
    $('#word').val('');
    if (word.length<=20 && word.length >0){
        $('#chat_panel').append(
            '<div class="ui raised segment" style="padding-bottom: 0;text-align: left;border: 2px solid black">' +
            '<p style="float: right">'+year+'-'+mon+'-'+date+' '+h+':'+m+'</p>' +
            '<pre style="font-size: 14px;font-family: 微软雅黑">'+word+'</pre>' +
            '</div>');
        $.ajax({
            type : "POST",
            dataType: "json",
            url : Voice_URL.dataTextChat,
            data : {'word':word},
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
    }
    else{
        alert('输入字数限二十字以内！')
    }
});
/**
 *语音合成
 * */
$('#composite').click(function () {
    let text = $('#composite_text').val();
    if (text.length<=200 && text.length >0){
        $.ajax({
            type : "POST",
            dataType: "json",
            url : Voice_URL.dataTextComposite,
            data : {'text':text},
            success : function(data) {
                if (data.ret){
                    $('#composite_text').val('');
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
    }else {
        alert('字数限制在二百字以内！')
    }
});
/**
 * 录音播放
 * */
// let time_func;
// // let recognize_params = $('#recognize_params').val();
// if (recognize_params){
//     console.log(recognize_params)
// }
function btn_show(){
    $('#btn_start_audio').attr('disabled', false);
    $('#countdown').hide()
}
$('#btn_start_audio').click(function () {
    $('#btn_start_audio').attr('disabled', true);
    $('#countdown').show();
    $('#countdown').timeTo({
        seconds: 30,
        displayHours: false,
        fontSize: 40,
        captionSize: 14,
        theme:'red'
    });
    clearTimeout(time_func);
    time_func = setTimeout(btn_show, 30000);
});
$('#btn_stop_audio').click(function () {
    btn_show()
});


// $('#btn_start').click(function () {
//     $('#btn_start').hide();
//     $('#countdown').show();
//     $('#countdown').timeTo({
//         seconds: 30,
//         displayHours: false,
//         fontSize: 40,
//         captionSize: 14,
//         theme:'red'
//     })
// });
// $('#btn_stop').click(function () {
//     $('#countdown').hide()
// });
$('.btn_audio').click(function () {
    $.ajax(
        {
            type : "POST",
            dataType: "json",
            url : Voice_URL.dataVoiceAudioPlay,
            data : {'operate':this.value},
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
        }
    )
});
/**
 * 控制对话
 **/
$('.btn_voice').click(function () {
    $.ajax(
        {
            type : "POST",
            dataType: "json",
            url : Voice_URL.dataCommand,
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
        }
    )
});

/**
 * 语音识别
 * */
// let time_func;
// let recognize_params = $('#recognize_params').val();
// if (recognize_params){
//     console.log(recognize_params)
// }
function btn_recognize_show(){
    $('#btn_start_recognize').attr('disabled', false);
    // $('#countdown').hide()
}
$('#btn_start_recognize').click(function () {
    $('#btn_start_recognize').attr('disabled', true);
    // $('#countdown').show();
    // $('#countdown').timeTo({
    //     seconds: 10,
    //     displayHours: false,
    //     fontSize: 40,
    //     captionSize: 14,
    //     theme:'red'
    // });
    // clearTimeout(time_func);
    time_func = setTimeout(btn_show, 10000);
});
$('#btn_stop_recognize').click(function () {
    btn_recognize_show()
});

$('.btnn').click(function () {
    let param = this.value;
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Voice_URL.dataRecognize,
        data : {'operate':param},
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
    }
);
