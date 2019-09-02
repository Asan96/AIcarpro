$('.show_btn').click(function () {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : ImgShowUrl.dataImgShow,
        data : {'order':this.value, 'img_path':img_path},
        success : function(data) {
            if (data.ret){
                $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
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
});