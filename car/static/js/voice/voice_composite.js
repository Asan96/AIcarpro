$('#composite').click(function () {
    let text = $('#composite_text').val();
    if (text.length<=30 && text.length >0){
        $.ajax({
            type : "POST",
            dataType: "json",
            url : PUB_URL.dataTextComposite,
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
    }
});