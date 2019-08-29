let time_func;
let recognize_params = $('#recognize_params').val();
if (recognize_params){
    console.log(recognize_params)
}
function btn_show(){
    $('#btn_start').attr('disabled', false);
    $('#countdown').hide()
}
$('#btn_start').click(function () {
    $('#btn_start').attr('disabled', true);
    $('#countdown').show();
    $('#countdown').timeTo({
        seconds: 10,
        displayHours: false,
        fontSize: 40,
        captionSize: 14,
        theme:'red'
    });
    clearTimeout(time_func);
    time_func = setTimeout(btn_show, 10000);
});
$('#btn_stop').click(function () {
    btn_show()
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
