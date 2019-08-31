$('#btn_open_file').click(function () {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataOpenImageFile,
        data : {},
        success : function(data) {
            if (data.ret){
                console.log(data.msg);
                console.log(typeof data.msg)
                let img = document.getElementById("img_main");
                $('#img_main').show();
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