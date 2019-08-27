
$('#send').click(function () {
    let word = $('#word').val();
    if (word.length<=20 && word.length >0){
        $('#chat_panel').append('<div class="ui raised segment font_left"><pre>'+word+'</pre></div>')
    }
    else{
        // alert('输入字数限二十字以内！')
        swal(1111111)

    }
});
