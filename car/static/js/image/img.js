let color;
let reg=/^[0-9]+.?[0-9]*$/;
let loading_path = '/static/plugin/img/loading.gif';
/* 数字判断*/
function regix(num_lst){
    for(let i =0;i<num_lst.length;i++)
    {
        let num = num_lst[i];
        if(!num||!reg.test(num)||num<0){
            return false
        }
    }
    return true
}
let img_path = $('#img_main' ).attr('src');
let show_flag = 0;
$('#btn_upload_file').click(function () {
    $('#file_upload').trigger('click');
});
$('#file_upload').change(function () {
    let form_data = new FormData();
    let file_info =$( '#file_upload')[0].files[0];
    let fileSize = 0;
    let fileType = '';
    if (file_info){
        fileSize = (file_info.size / 1024).toFixed(0);
        fileType = file_info.name.substring(file_info.name.lastIndexOf("."));
    }
    let typeArray = ['.jpg','.jpeg', '.png'];
    if (fileSize > 10240){
        alert('图片文件过大，请选择10M以下的图片');
        return;
    }
    if ($.inArray(fileType,typeArray) === -1){
        alert('请选择jpg、jpeg或png格式的图片！');
        return
    }
    form_data.append('file',file_info);
    $('.div_base').hide();
    hide_operation();
    show_flag = 0;
    $.ajax({
        url: Image_URL.dataUpload,
        type:'POST',
        data: form_data,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function(response) {
            if (response.ret){
                img_path = response.msg;
                $('#img_main').attr('src', response.msg.split('car')[1]+'?'+Math.random());
                if (!show_flag){
                    $('.before_btn').attr('disabled',true)
                }
            }
            else {
                alert(response.msg)
            }
        },
        error : function(e){
            console.log(e);
        }
    });
});

/**
 * 隐藏其他操作
 * */
function hide_operation(){
    $('.div_base').hide();
    $('.draw').hide();
    $('#div_draw').hide();
}
/**
 * 代码展示
 * */
let editor;
let version = "#!/usr/bin/python\n# coding=utf-8\n# version: Python3\n";
let tone_word = "# 执行图片处理操作，显示对应操作的主要代码\n";
let initValue = version+tone_word;
window.onload = function () {
    let el = document.getElementById("code_text");
    editor = CodeMirror.fromTextArea(el, {
        theme: 'eclipse', //编辑器主题
        mode: "text/x-python", // 语言模式
        keyMap: "sublime", // 快键键风格
        lineNumbers: true, // 显示行号
        smartIndent: true, // 智能缩进
        indentUnit: 4, // 智能缩进单位为4个空格长度
        indentWithTabs: true, // 使用制表符进行智能缩进
        lineWrapping: true, //
        // 在行槽中添加行号显示器、折叠器、语法检测器
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
        foldGutter: true, // 启用行槽中的代码折叠
        autofocus: false, // 自动聚焦
        matchBrackets: true, // 匹配结束符号
        autoCloseBrackets: true, // 自动闭合符号
        styleActiveLine: true, // 显示选中行的样式
    });
    editor.setSize('auto','90%');
    editor.replaceSelection(initValue);
    editor.on("keypress", function() {
        editor.showHint(); // 注释show-hint.js第132行，阻止自动补全
    })
};
$('.codeCls').click(function () {
    let key = this.value;
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataImgCode,
        data : {'key':key},
        success : function(data) {
            if (data.ret){
                console.log(data.msg);
                editor.setValue(data.msg)
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

/**
 * 调色板初始化
 * */
$('.paigusu').paigusu({
    color : '#1926dc',
},function(event,obj){
    // console.log(event);
    // console.log(obj.rgb);
    color = obj.rgb;

    $(event).css('color','#' + obj.hex)
});
/**
 * 通过id给params字典添加键值对
 * */
function addParams(params,arr) {
    for(let i =0;i<arr.length;i++){
        params[arr[i]] = $('#'+arr[i]).val()
    }
    return params
}
/**
 * 根据id判断元素值是否为正整数
 * */
function judgeNum(arr) {
    for (let i =0; i<arr.length;i++){
        let num = Number($('#'+arr[i]).val());
        if(!num||!reg.test(num)||num<0){
            return false
        }
    }
    return true
}
/**
 * 清空class的值
 * */
function clear(class_arr) {
    for (let i =0;i<class_arr.length;i++){
        $('.'+class_arr[i]).val('')
    }
}


$('.before_btn').attr('disabled',true);
$('.show_btn').click(function () {
    hide_operation();
    if (this.value === 'gray_img'||this.value === 'color_img'){
        show_flag = 1;
        $('.before_btn').attr('disabled',false)
    }
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataImgShow,
        data : {'order':this.value, 'img_path':img_path},
        success : function(data) {
            if (data.ret){
                if (data.type === 1){
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


$('.btn_base').click(function () {
    hide_operation();
    let order = this.value;
    let params;
    params = {
        'img_path': img_path,
        'order': order
    };
    let origin_path = img_path;
    if(img_path.startsWith('car')){
        origin_path = img_path.split('car')[1]
    }
    $('#img_main').attr('src', origin_path +'?'+Math.random());
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
function post_base(params) {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataImgBase,
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
                        callback_extended_fillet(data);
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
    if (data.error){
        $('#img_main').attr('src', data.path.split('car')[1]+'?'+Math.random());
        alert(data.msg)
    }else{
        $('#img_main').attr('src', data.path.split('car')[1]+'?'+Math.random());
    }
    $('#btn_boundary').attr('disabled',false);
}

$('#btn_clear_pixel').click(function () {
    clear(['coordinate'])
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

/**
 * 绘图函数
 * **/
$('#btn_clear').click(function () {
    $('.coordinate').val('');
    $('.color_RGB').val('');
    let clear_path = img_path;
    if(img_path.startsWith('car')){
        clear_path = img_path.split('car')[1]
    }
    $('#img_main').attr('src', clear_path);
});
let operate;
$('.paint_btn').click(function () {
    hide_operation();
    operate = this.value;
    $('#'+operate).show();
    $('#div_draw').show()
});

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
        url : Image_URL.dataImgDraw,
        data : params,
        success : function(data) {
            if (data.ret){
                $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
                img_path = data.msg;
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
