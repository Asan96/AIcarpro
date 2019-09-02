let img_path = $('#img_main').attr('src');
$('#btn_open_file').click(function () {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataOpenImageFile,
        data : {},
        success : function(data) {
            if (data.ret){
                console.log(data.msg);
                img_path = data.msg;
                $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
            }
            else{
                console.log(data.msg)
            }
        },
        error : function(e){
            console.log(e);
        }
    });
});