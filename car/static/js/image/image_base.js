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
            post_data(params)
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
                        td_attribute(data)
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
    $('#dtype').text(data.dtype);
    $('#size').text(data.size)
}