
$('#send').click(function () {
    let word = $('#word').val();
    $('#word').val('');
    if (word.length<=20 && word.length >0){
        $('#chat_panel').append('<div class="ui raised segment font_left"><pre>'+word+'</pre></div>')
        $.ajax({
            type : "POST",
            dataType: "json",
            url : PUB_URL.dataTextChat,
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
