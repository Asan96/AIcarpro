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
                let change_pixel_params = ['pixel_x', 'pixel_y'];
                if (!judgeNum(change_pixel_params)){
                    alert('位置坐标请输入正整数！')
                }else if(!color){
                    alert('请选择像素值！')
                }
                else {
                    params = addParams(params, change_pixel_params);
                    params['color'] = color;
                    post_data(params)
                }

            });
            break;
        case "img_roi":
            let show_roi_params = ['pixel_x1','pixel_x2','pixel_y1','pixel_y2'];
            $('#btn_show_roi').click(function () {
                if(!judgeNum(show_roi_params)){
                    alert('截取矩形ROI范围必须为正整数！')
                }
                else{
                    params = addParams(params, show_roi_params);
                    params['type'] = 'show';
                    post_data(params)
                }
            });
            let move_roi_params = ['pixel_x1','pixel_x2','pixel_y1','pixel_y2','pixel_x3','pixel_x4','pixel_y3','pixel_y4'];
            $('#btn_move_roi').click(function () {
                if(!judgeNum(move_roi_params)){
                    alert('移动目标范围必须为正整数！')
                }
                else{
                    params = addParams(params, move_roi_params);
                    params['type'] = 'move';
                    post_data(params)
                }
            });
            break;
        case "extended_fillet":
            $('#btn_boundary').click(function () {
                params['side'] = $('#side').val();
                post_data(params)
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
                        callback_attribute(data);
                    case "change_pixel":
                        callback_change_pixel(data);
                    case "img_roi":
                        callback_image_roi(data);
                    case "extended_fillet":
                        callback_extended_fillet(data)
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
function callback_attribute(data) {
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

function callback_change_pixel(data) {
    $('#div_pixel').show();
    $('#old_pixel').text(data.old_pixel);
    $('#new_pixel').text(data.new_pixel);
}

function callback_image_roi(data){
    if (data.order === 'move'){
        $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
    }
}

function callback_extended_fillet(data){
    $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
}

$('#btn_clear_pixel').click(function () {
    $('.coordinate').val('');
});


$('#btn_clear_roi1').click(function () {
    $('.coordinate_show').val('')
});
$('#btn_clear_roi2').click(function () {
    $('.coordinate_move').val('')
});