$('.btn_base').click(function () {
    $('.div_base').hide();
    let order = this.value;
    let params = {
        'img_path': img_path,
        'order': order
    };
    $('#'+order).show();
    switch (order) {
        case "attribute":
            post_data(params);
            break;
        case "change_pixel":
            $('#div_pixel').hide();
            $('#btn_change_pixel').click(function () {
                let params_arr = ['pixel_x', 'pixel_y']
                if (!judgeNum(params_arr)){
                    alert('位置坐标请输入正整数！')
                }else if(!color){
                    alert('请选择像素值！')
                }
                else {
                    params = addParams(params, params_arr);
                    params['color'] = color;
                    post_data(params)
                }

            });
            break;
        case "img_roi":
            let params_arr1 = ['pixel_x1','pixel_x2','pixel_y1','pixel_y2'];
            $('#btn_show_roi').click(function () {
                if(!judgeNum(params_arr1)){
                    alert('坐标必须为正整数！')
                }
                else{
                    params = addParams(params, params_arr1);
                    post_data(params)
                }
            })

    }
});
$('#btn_open_file').click(function () {
    $('.div_base').hide();
});
function post_data(params) {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : ImgBaseUrl.dataImgBase,
        data : params,
        success : function(data) {
            if (data.ret){
                switch (data.type) {
                    case "attribute":
                        td_attribute(data);
                    case "change_pixel":
                        callback_change_pixel(data)
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
}
function td_attribute(data) {
    let shape = data.shape;
    $('#suffix').text(img_path.split('.')[1]);
    $('#row').text(shape[0]);
    $('#col').text(shape[1]);
    if (shape.length === 3){
        $('#aisle').text(shape[2])
    }
    $('#size').text(shape[1]+'x'+shape[0]);
    $('#dtype').text(data.dtype);
    $('#pixel').text(data.pixel);
}

$('#btn_clear_pixel').click(function () {
    $('.coordinate').val('');
});

function callback_change_pixel(data) {
    $('#div_pixel').show();
    $('#old_pixel').text(data.old_pixel);
    $('#new_pixel').text(data.new_pixel);
}

