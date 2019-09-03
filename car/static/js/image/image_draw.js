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
function regix_RGB(num_lst){
        for(let i =0;i<num_lst.length;i++)
    {
        let num = num_lst[i]
        if(!num||!reg.test(num)||num<0||num>255){
            return false
        }
    }
    return true
}
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
    let R = $('#color_R').val()
    let G = $('#color_G').val()
    let B = $('#color_B').val()
    if (!regix_RGB([R,G,B])){
        alert('颜色必须为0-255之间的正整数！')
    }else{
        params = {
            'operate': operate,
            'img_path': img_path,
            'R': R,
            'G': G,
            'B': B,
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
