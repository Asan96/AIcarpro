$('.before_btn').attr('disabled',true)
$('.show_btn').click(function () {
    if (this.value === 'gray_img'||this.value === 'color_img'){
        show_flag = 1;
        $('.before_btn').attr('disabled',false)
    }
    $.ajax({
        type : "POST",
        dataType: "json",
        url : ImgShowUrl.dataImgShow,
        data : {'order':this.value, 'img_path':img_path},
        success : function(data) {
            if (data.ret){
                if (data.type == 1){
                    $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
                }
            }
            else{
                alert(data.msg)
            }
        },
        error : function(e){
            console.log(e.status);
            console.log(e.responseText);
        }
    });
});