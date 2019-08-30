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