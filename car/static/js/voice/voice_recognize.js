$('.btnn').click(function () {
    let param = this.value();
    $.ajax({
        type : "POST",
        dataType: "json",
        url : PUB_URL.dataRecognize,
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