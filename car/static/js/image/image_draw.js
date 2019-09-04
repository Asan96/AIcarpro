let operate = 'draw_line';
let reg=/^[0-9]+.?[0-9]*$/;
$('#btn_clear').click(function () {
    $('.coordinate').val('')
    $('.color_RGB').val('')
});
$('.checkbox').change(
    function () {
        operate = $(this).children('input').val()
        $('.draw').hide()
        $('#'+operate).show()
    }
);
function regix(num_lst){
    for(let i =0;i<num_lst.length;i++)
    {
        let num = num_lst[i]
        console.log(num)
        if(!num||!reg.test(num)||num<0){
            return false
        }
    }
    return true
}
$('#btn_draw').click(function () {
    let params;
    if (!color){
        alert('请选择绘制图形的颜色！')
    }
    else{
        params = {
            'operate': operate,
            'img_path': img_path,
            'color':color,
        }
    }
    switch (operate) {
        case "draw_line":
            let start_x = $('#line_start_x').val()
            let start_y = $('#line_start_y').val()
            let end_x = $('#line_end_x').val()
            let end_y = $('#line_end_y').val()
            if (!regix([start_x, start_y,end_x, end_y])){
                alert('坐标必须为正整数！')
            }
            else{
                params['start_x'] = start_x;
                params['start_y'] = start_y;
                params['end_x'] = end_x;
                params['end_y'] = end_y
                post_data(params)
            }
            break;
        case "draw_rectangle":
            let left_up_x = $('#left_up_x').val()
            let left_up_y = $('#left_up_y').val()
            let right_down_x = $('#right_down_x').val()
            let right_down_y = $('#right_down_y').val()
            if(!regix([left_up_x, left_up_y, right_down_x, right_down_y])){
                alert('坐标必须为正整数！')
            }
            else{
                params['left_up_x'] = left_up_x
                params['left_up_y'] = left_up_y
                params['right_down_x'] = right_down_x
                params['right_down_y'] = right_down_y
                post_data(params)
            }
            break
        case "draw_circle":
            let circle_x = $('#circle_x').val()
            let circle_y = $('#circle_y').val()
            let circle_r = $('#circle_r').val()
            if(!regix([circle_x, circle_y, circle_r])){
                alert('坐标和半径必须为正整数！')
            }
            else{
                params['circle_x'] = circle_x
                params['circle_y'] = circle_y
                params['circle_r'] = circle_r
                post_data(params)
            }
            break
        case "draw_oval":
            let oval_x = $('#oval_x').val()
            let oval_y = $('#oval_y').val()
            let oval_a = $('#oval_a').val()
            let oval_b = $('#oval_b').val()
            let oval_angle = $('#oval_angle').val()
            let oval_start_angle = $('#oval_start_angle').val()
            let oval_end_angle = $('#oval_end_angle').val()
            if (!regix([oval_x,oval_y,oval_a,oval_b,oval_angle,oval_start_angle,oval_end_angle])){
                alert('坐标、长度角度必须为正整数！')
            }else{
                params['oval_x'] = oval_x
                params['oval_y'] = oval_y
                params['oval_a'] = oval_a
                params['oval_b'] = oval_b
                params['oval_angle'] = oval_angle
                params['oval_start_angle'] = oval_start_angle
                params['oval_end_angle'] = oval_end_angle
                post_data(params)
            }
            break
        case "draw_ploygon":
            let ploygon_x1 = $('#ploygon_x1').val()
            let ploygon_y1 = $('#ploygon_y1').val()
            let ploygon_x2 = $('#ploygon_x2').val()
            let ploygon_y2 = $('#ploygon_y2').val()
            let ploygon_x3 = $('#ploygon_x3').val()
            let ploygon_y3 = $('#ploygon_y3').val()
            let ploygon_x4 = $('#ploygon_x4').val()
            let ploygon_y4 = $('#ploygon_y4').val()
            if (!regix([ploygon_x1,ploygon_y1,ploygon_x2,ploygon_y2,ploygon_x3, ploygon_y3,ploygon_x4,ploygon_y4])){
                alert('坐标必须为正整数！')
            }else {
                params['ploygon_x1'] = ploygon_x1
                params['ploygon_y1'] = ploygon_y1
                params['ploygon_x2'] = ploygon_x2
                params['ploygon_y2'] = ploygon_y2
                params['ploygon_x3'] = ploygon_x3
                params['ploygon_y3'] = ploygon_y3
                params['ploygon_x4'] = ploygon_x4
                params['ploygon_y4'] = ploygon_y4
                post_data(params)
            }
            break
        case "add_text":
            let words = $('#words').val()
            let add_text_x = $('#add_text_x').val()
            let add_text_y = $('#add_text_y').val()
            if (!regix([add_text_x, add_text_y])){
                alert('坐标必须为正整数！')
            }else{
                params['words'] = words
                params['add_text_x'] = add_text_x
                params['add_text_y'] = add_text_y
                post_data(params)
            }
            break
    }

});
function post_data(params) {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : ImgDrawUrl.dataImgDraw,
        data : params,
        success : function(data) {
            if (data.ret){
                $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
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
