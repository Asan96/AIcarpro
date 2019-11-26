let editor;
let version = "#!/usr/bin/python\n# coding=utf-8\n# version: Python3\n";
let codeAreaTip = "# please edit your code here:\n";
let initValue = version+codeAreaTip;
// let initValue = '';
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
    editor.setSize('auto','500px');
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

$('#btn_import').click(function () {
    $('#py_upload').trigger('click');
});
$('#py_upload').change(function () {
    let pyData = new FormData();
    let pyInfo =$( '#py_upload')[0].files[0];
    let pySize = 0;
    let pyType = '';
    if (pyInfo){
        pySize = (pyInfo.size / 1024).toFixed(0);
        pyType = pyInfo.name.substring(pyInfo.name.lastIndexOf("."));
    }
    if (pySize > 1024){
        alert('python 文件过大，请选择1M以下文件！');
        return;
    }
    if (pyType !== '.py'){
        alert('请选择 python文件！');
        return;
    }
    pyData.append('file',pyInfo);
    $.ajax({
        url: CodeURL.serialUploadPyFile,
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
        url : CodeURL.serialCodeRun,
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
        url : CodeURL.serialCodeOperate,
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

/**
 * 串口通信
**/

function realodDevices(){
    getDevicesList(
        function(response){
            $('#devices').empty();
            if(response.result === "ok"){
                for(let i = 0; i < response.ports.length; i++){
                    $('#devices').append('<option value="' + response.ports[i].path +  '">' + response.ports[i].displayName + '(' + response.ports[i].path + ')' + '</option>');
                }
            }
            else{
                alert(response.error);
            }
        }
    );
}

function openSelectedPort(){
    serialPort.openPort(
        {
            portName: $('#devices').val(),
            bitrate: 115200,
            dataBits: "eight",
            parityBit: "no",
            stopBits: "two"
        },
        function(response){
            console.log(response);
            if(response.result === "ok"){
                //Do something
            }
            else{
                alert(response.error);
            }
        }
    );
}

function closeCurrentPort(){
    serialPort.closePort(
        function(response){
            console.log(response);
            if(response.result === "ok"){
                //Do something
            }
            else{
                alert(response.error);
            }
        }
    );
}
let response_str = '';
function onNewData(data){
    let end_flag = "exec(open('mixly.py').read(),globals())";
    let str = "";
    let dv = new DataView(data);
    for(let i = 0; i < dv.byteLength; i++){
        str = str.concat(String.fromCharCode(dv.getUint8(i, true)));
    }
    response_str += str;
    if (response_str.indexOf(end_flag)>=0)
    {
        $('#console').empty().append('>>>'+response_str.split(end_flag).slice(-1));
    }

}

function sendData(){
    response_str = '';
    $('#console').val('');
    let code = editor.getValue();
    code = code.replace(/[\r\n]/g,"\\n").replace(/\n/g,'\\n').replace(/\t/g,'\\t'); //去掉回车换行;
    console.log(code)
    let mainCode = [
        "f= open('./mixly.py','wb+',encoding='utf-8')",
    ];
    for(let i =0;i<code.length;i+=100){
        mainCode.push('f.write(b"""'+code.slice(i,i+100)+'""")')
    }
    mainCode.push('f.close()');
    mainCode.push("exec(open('mixly.py').read(),globals())");
    for (let i = 0; i<mainCode.length;i++){
        setTimeout(() => {
            let input = stringToArrayBuffer(mainCode[i]+'\r');
            serialPort.write(input,
                function(response){
                    // console.log(response);
                }
            );
        }, 100*i);
    }
}

for (let i = 0; i < 10; i++) {

}

function stringToArrayBuffer(string){
    let buffer = new ArrayBuffer(string.length);
    let dv = new DataView(buffer);
    for(let i = 0; i < string.length; i++){
        dv.setUint8(i, string.charCodeAt(i));
    }
    return dv.buffer;
}

window.onbeforeunload = function(){
    if(serialPort.isOpen()){
        serialPort.closePort(
            function(response){
                console.log(response);
                if(response.result === "ok"){
                    return null;
                }
                else{
                    alert(response.error);
                    return false;
                }
            }
        );
    }
    return null;
};

/**
 * @version 1.0
 * Google Chrome browser app to allow the use of serial ports comunication inside a web page.
 *	The app acts as an wrapper between the web pages and the serial ports.
 * The app use the chrome.serial API to interact with the serial ports and
 * the chrome.runtime messaging API to exchange information with the web page.
 * It is also provided a simple JavaScript library to use inside the web pages to access the services offered by the app.
 */

/**
 * Extension unique id to start the comunication.
 */
let extensionId = "helkffleffnhhnoepaimiaebdcagpllc";

function SerialPort(){
    /**
     * Port GUID assigned by the app.
     */
    let portGUID;

    /**
     * Initialize the comunication with the app.
     */
    let port = chrome.runtime.connect(extensionId);

    /**
     * Contain the unique serial port connection id.
     */
    let serialConnectionId;

    /**
     * Bool that indicates if the serial connection is open.
     */
    let isSerialPortOpen = false;

    /**
     * Callback function to call if there is new data incoming from the serial port connection.
     */
    let onDataReceivedCallback = undefined;

    /**
     * Callback function to call if there is the connection encountered some problems.
     */
    let onErrorReceivedCallback = undefined;

    /**
     * Listener to handle incoming message from the app trought the messaging port.
     * Handled commands are:
     * - guid -> received when the connection with the app is established, represent the GUID assigned to the port
     * - serialdata -> received when new binary data is available on the serial port
     */
    port.onMessage.addListener(
        function(msg) {
            if(msg.header === "guid"){
                portGUID = msg.guid;
            }
            else if(msg.header === "serialdata"){
                if(onDataReceivedCallback !== undefined){
                    onDataReceivedCallback(new Uint8Array(msg.data).buffer);
                }
            }
            else if(msg.header === "serialerror"){
                onErrorReceivedCallback(msg.error);
            }
        }
    );

    /**
     * Check if the current port is opened.
     */
    this.isOpen = function(){
        return isSerialPortOpen;
    }

    /**
     * Set the new data callback.
     */
    this.setOnDataReceivedCallback = function(callBack){
        onDataReceivedCallback = callBack;
    }

    /**
     * Set the error callback.
     */
    this.setOnErrorReceivedCallback = function(callBack){
        onErrorReceivedCallback = callBack;
    }

    /**
     * Try to open a serial connection.
     * portInfo MUST contain:
     * portName -> path to the port to open
     * bitrate -> port bit rate as number
     * dataBits -> data bit ("eight" or "seven")
     * parityBit -> parity bit ("no", "odd" or "even")
     * stopBits -> stop bit ("one" or "two")
     * Callback is a function to call to handle the app result.
     */
    this.openPort = function(portInfo, callBack){
        chrome.runtime.sendMessage(extensionId,
            {
                cmd: "open",
                portGUID: portGUID,
                info: portInfo
            },
            function(response){
                if(response.result === "ok"){
                    isSerialPortOpen = true;
                    serialConnectionId = response.connectionInfo.connectionId;
                }
                callBack(response);
            }
        );
    }

    /**
     * Try to close the serial connection.
     * Callback is a function to call to handle the app result.
     */
    this.closePort = function(callBack){
        chrome.runtime.sendMessage(extensionId,
            {
                cmd: "close",
                connectionId: serialConnectionId
            },
            function(response){
                if(response.result === "ok"){
                    isSerialPortOpen = false;
                }
                callBack(response);
            }
        );
    }

    /**
     *	Write data on the serial port.
     * The request MUST contain:
     * connectionId -> connection unique id provided when the port is opened
     * data -> Array which contains the bytes to send
     */
    this.write = function(data, callBack){
        chrome.runtime.sendMessage(extensionId,
            {
                cmd: "write",
                connectionId: serialConnectionId,
                data: Array.prototype.slice.call(new Uint8Array(data))
            },
            function(response){
                if(response.result === "ok"){
                    if(response.sendInfo.error !== undefined){
                        if(response.sendInfo.error === "disconnected" || response.sendInfo.error === "system_error"){
                            isSerialPortOpen = false;
                            closePort(function(){});
                        }
                    }
                }
                callBack(response);
            }
        );
    }
}

/**
 *	Get the list of all serial devices connected to the pc.
 * If there is no error it will return an array of object containing:
 * - path
 * - vendorId (optional)
 * - productId (optional)
 * - displayName (optional)
 * Callback is a function to call to handle the app result.
 */
function getDevicesList(callBack){
    chrome.runtime.sendMessage(extensionId, {cmd: "list"}, callBack);
}

/**
 * Used to check if the Serial Interface app is installed on the browser.
 * If it's installed return result: "ok" and the current version
 */
function isExtensionInstalled(callback){
    chrome.runtime.sendMessage(extensionId, { cmd: "installed" },
        function (response) {
            if (response){
                callback(true);
            }else{
                callback(false);
            }
        }
    );
}

