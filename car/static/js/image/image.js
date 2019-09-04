let color;
let reg=/^[0-9]+.?[0-9]*$/;
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

let img_path = $('#img_main').attr('src');
let show_flag = 0;
/**
 * 打开文件
 * */
$('#btn_open_file').click(function () {
    show_flag = 0;
    $.ajax({
        type : "POST",
        dataType: "json",
        url : Image_URL.dataOpenImageFile,
        data : {},
        success : function(data) {
            if (data.ret){
                img_path = data.msg;
                $('#img_main').attr('src', data.msg.split('car')[1]+'?'+Math.random());
                if (!show_flag){
                    $('.before_btn').attr('disabled',true)
                }
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
        let num = $('#'+arr[i]).val();
        if(!num||!reg.test(num)||num<0){
            return false
        }
    }
    return true
}