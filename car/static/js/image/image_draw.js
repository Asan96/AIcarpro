let operate = 'draw_line';
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
            let line_params = ['line_start_x', 'line_start_y', 'line_end_x', 'line_end_y']
            if (!judgeNum(line_params)){
                alert('坐标必须为正整数！')
            }
            else{
                params = addParams(params,line_params)
                post_data(params)
            }
            break;
        case "draw_rectangle":
            let rectangle_params = ['left_up_x', 'left_up_y', 'right_down_x', 'right_down_y'];
            if(!judgeNum(rectangle_params)){
                alert('坐标必须为正整数！')
            }
            else{
                params = addParams(params, rectangle_params)
                post_data(params)
            }
            break
        case "draw_circle":
            let circle_params = ['circle_x', 'circle_y', 'circle_r'];
            if(!judgeNum(circle_params)){
                alert('坐标和半径必须为正整数！')
            }
            else{
                addParams(params,circle_params);
                post_data(params)
            }
            break
        case "draw_oval":
            let oval_params = ['oval_x', 'oval_y', 'oval_a','oval_b','oval_angle','oval_start_angle', 'oval_end_angle'];
            if (!judgeNum(oval_params)){
                alert('坐标、长度角度必须为正整数！')
            }else{
                params = addParams(params, oval_params);
                post_data(params)
            }
            break
        case "draw_ploygon":
            let ploygon_params = ['ploygon_x1','ploygon_y1','ploygon_x2','ploygon_y2','ploygon_x3','ploygon_y3','ploygon_x4','ploygon_y4']
            if (!judgeNum(ploygon_params)){
                alert('坐标必须为正整数！')
            }else {
                addParams(params, ploygon_params);
                post_data(params)
            }
            break
        case "add_text":
            let words = $('#words').val()
            let text_params = ['add_text_x', 'add_text_y'];
            if (!judgeNum(text_params)){
                alert('坐标必须为正整数！')
            }else{
                params = addParams(params, text_params);
                params['words'] = words;
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
