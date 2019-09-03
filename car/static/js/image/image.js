let img_path = $('#img_main').attr('src');
let show_flag = 0;
$('#btn_open_file').click(function () {
    show_flag = 0;
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataOpenImageFile,
        data : {},
        success : function(data) {
            if (data.ret){
                img_path = data.msg;
                $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
                if (!show_flag){
                    $('.before_btn').attr('disabled',true)
                }
            }
            else{
                alert(data.msg)
            }
        },
        error : function(e){
            console.log(e);
        }
    });
});