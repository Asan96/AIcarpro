let editor;
let version = "#!/usr/bin/python\n# coding=utf-8\n# version: Python3\n";
let codeAreaTip = "# please edit your code here:\n";
let initValue = version+codeAreaTip;
window.onload = function () {
    let el = document.getElementById("editor");
    editor = CodeMirror.fromTextArea(el, {
        theme: 'darcula', //编辑器主题
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
        autofocus: true, // 自动聚焦
        matchBrackets: true, // 匹配结束符号
        autoCloseBrackets: true, // 自动闭合符号
        styleActiveLine: true, // 显示选中行的样式
    });
    editor.setSize('auto','600px');
    editor.replaceSelection(initValue);
    editor.on("keypress", function() {
        editor.showHint(); // 注释show-hint.js第132行，阻止自动补全
    })
};
$('#btn_clear').click(function () {
    editor.setValue(initValue);
    $('#console').text('')
});
$('#btn_run').click(function () {
    $('#console').text('正在执行中。。。。。。')
    let code = editor.getValue();//获取经过转义的编辑器文本内容
    let params = {
        'code':code,
        'isCar': 0,
        'type': 'run',
    };
    post_code(params)

});
$('#btn_stop').click(function () {
    post_code({'type':'stop'})
});
$('#btn_run_in_car').click(function () {
    $('#console').text('正在小车上执行。。。。。。');
    setTimeout(function(){
        $('#console').text('');
    }, 2000);
    let code = editor.getValue();
    $('#btn_stop i').attr('class','icon red stop');
    let params = {
        'code':code,
        'isCar':1,
        'type': 'run',
    };
    post_code(params)
});
$('#btn_import').click(function () {
    $('#py_upload').trigger('click');
});
$('#py_upload').change(function () {
    let pyData = new FormData();
    let pyInfo =$( '#py_upload')[0].files[0];
    console.log(pyInfo)
    let pySize = 0;
    let pyType = '';
    if (pyInfo){
        pySize = (pyInfo.size / 1024).toFixed(0);
        pyType = pyInfo.name.substring(pyInfo.name.lastIndexOf("."));
    }
    if (pySize > 1024){
        alert('图片文件过大，请选择10M以下的图片');
        return;
    }
    if (pyType !== '.py'){
        alert('请选择 python文件！');
        return;
    }
    pyData.append('file',pyInfo);
    $.ajax({
        url: CodeURL.uploadPyFile,
        type:'POST',
        data: pyData,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
        success: function(response) {
            if (response.ret){
                editor.setValue(response.msg)
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

$('#btn_save').click(function () {
    let code = editor.getValue();
    post_operate({'operate':'save', 'code':code})
});
function post_code(params) {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : CodeURL.dataCodeRun,
        data : params,
        success : function(data) {
            if (data.ret){
                if (data.type === 'local'){
                    print(data.msg)
                }
            }
            else{
                print(data.msg)
            }
        },
        error : function(e){
            console.log(e.status);
            console.log(e.responseText);
        }
    });
}
function post_operate(params) {
    $.ajax({
        type : "POST",
        dataType: "json",
        url : CodeURL.dataCodeOperate,
        data : params,
        success : function(data) {
            if (data.ret){
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

function print(msg) {
    $('#console').text(msg)
}