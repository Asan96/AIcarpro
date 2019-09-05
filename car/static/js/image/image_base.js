$('.btn_base').click(function () {
    $('.div_base').hide();
    let order = this.value;
    let params;
    params = {
        'img_path': img_path,
        'order': order
    };
    console.log(params);
    clear(['coordinate', 'coordinate_show', 'coordinate_move','side']);
    $('#'+order).show();
    switch (order) {
        case "attribute":
            post_base(params);
            break;
        case "change_pixel":
            change_pixel_func(params);
            break;
        case "img_roi":
            img_roi_func(params);
            break;
        case "extended_fillet":
            extended_fillet_func(params);
            break;


    }
});
$('#btn_open_file').click(function () {
    $('.div_base').hide();
});
function post_base(params) {
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
                        break;
                    case "change_pixel":
                        callback_change_pixel(data);
                        break;
                    case "img_roi":
                        callback_image_roi(data);
                        break;
                    case "extended_fillet":
                        callback_extended_fillet(data)
                        break;
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
    $('#btn_boundary').attr('disabled',false);
}

$('#btn_clear_pixel').click(function () {
    clear(['coordinate'])
});


$('#btn_clear_roi1').click(function () {
    clear(['coordinate_show'])

});
$('#btn_clear_roi2').click(function () {
    clear(['coordinate_move'])
});

function change_pixel_func(params) {
    $('#div_pixel').hide();
    $('#btn_change_pixel').unbind().click(function () {
        $('#div_pixel').hide();
        let change_pixel_params = ['pixel_x', 'pixel_y'];
        if (!judgeNum(change_pixel_params)){
            alert('位置坐标请输入正整数！')
            return 0
        }else if(!color){
            alert('请选择像素值！')
            return 0
        }
        else {
            params = addParams(params, change_pixel_params);
            params['color'] = color;
            post_base(params)
            return 0
        }
    });
}
/**
 * 内部click 需要解绑上次的click
 * */
function img_roi_func(params) {
    let show_roi_params = ['pixel_x1','pixel_x2','pixel_y1','pixel_y2'];
    $('#btn_show_roi').unbind().click(function () {
        if(!judgeNum(show_roi_params)){
            alert('截取矩形ROI范围必须为正整数！')
        }
        else{
            params = addParams(params, show_roi_params);
            params['type'] = 'show';
            post_base(params)
        }
    });
    let move_roi_params = ['pixel_x1','pixel_x2','pixel_y1','pixel_y2','pixel_x3','pixel_x4','pixel_y3','pixel_y4'];
    $('#btn_move_roi').unbind().click(function () {
        if(!judgeNum(move_roi_params)){
            alert('移动目标范围必须为正整数！')
        }
        else{
            params = addParams(params, move_roi_params);
            params['type'] = 'move';
            post_base(params)
        }
    });
}
function extended_fillet_func(params) {
    $('#btn_boundary').unbind().click(function () {
        $('#btn_boundary').attr('disabled',true);
        if(!judgeNum(['side'])){
            alert('边界宽度必须为正整数！')
        }
        else{
            params['side'] = $('#side').val();
            $('#img_main').attr('src', loading_path+'?'+Math.random());
            post_base(params)
        }
    })
}