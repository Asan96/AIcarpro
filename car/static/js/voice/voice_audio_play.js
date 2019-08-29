$('#btn_start').click(function () {
    $('#countdown').show();
    $('#countdown').timeTo({
        seconds: 10,
        displayHours: false,
        fontSize: 40,
        captionSize: 14,
        theme:'red'
    })
});
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