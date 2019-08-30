$('.btn_voice').click(function () {
    $.ajax(
        {
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
        }
    )
});