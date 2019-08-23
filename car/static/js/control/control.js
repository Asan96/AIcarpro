$(function () {
    $('.btn').attr('disabled',true);
});
$('#car_switch').change(function () {
    let swit = $('#car_switch').prop("checked")
    console.log(swit)
    if (swit){
        $('.btn').attr('disabled',false)
    }
    else {
        $('.btn').attr('disabled',true);
    }
});

$('.btn').click(function () {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.dataControlCommand,
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
    console.log(this.value)
});
