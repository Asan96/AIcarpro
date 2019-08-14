$('#open_camera').click(
    function () {
        $('#open_camera').hide()
        $('#close_camera').show()
        var t=setTimeout("connect()",5000)
        $.ajax({
            type : "POST",
            dataType: "json",
            url : PUB_URL.dataGetHost,
            data : {'open': '1'},
            success : function(data) {
                console.log('1111111111111111')
                console.log(data);
                if (data.ret){
                    console.log('正在建立连接。。。')
                }
                else{
                    console.log(data.msg)
                }
            },
            error : function(e){
                console.log(e.status);
                console.log(e.responseText);
            }
        });
    }
);
function connect(){
    let conn = new WebSocket("ws://127.0.0.1:36660/");
    conn.onopen = function (evt) {
        console.log('客户端成功建立连接。。')
    };
    // conn.onmessage = function (evt) {
    //     let bytes = new Uint8Array(evt.data);
    //     let data = "";
    //     let len = bytes.byteLength;
    //     for (let i = 0; i < len; ++i) {
    //         data += String.fromCharCode(bytes[i]);
    //     }
    //     let img = document.getElementById("target");
    //     img.src = "data:image/jpg;base64,"+window.btoa(data);
    // };
    conn.onclose = function() {
        console.log("Closed");
    };

    conn.onerror = function(err) {
        console.log("Error: " + err);
    }}

//     var getUserMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
//
//     var video = document.getElementById('video');
//     var canvas = document.getElementById('canvas');
//     var ctx = canvas.getContext('2d');
//
//     getUserMedia.call(navigator, {
//         video: true,
//         audio: true
//     }, function(localMediaStream) {
//         video.src = window.URL.createObjectURL(localMediaStream);
//         video.onloadedmetadata = function(e) {
//             console.log("Label: " + localMediaStream.label);
//             console.log("AudioTracks" , localMediaStream.getAudioTracks());
//             console.log("VideoTracks" , localMediaStream.getVideoTracks());
//         };
//     }, function(e) {
//         console.log('Reeeejected!', e);
//     });
//
//     function dataURItoBlob(dataURI) {
//         // convert base64/URLEncoded data component to raw binary data held in a string
//         var byteString;
//         if (dataURI.split(',')[0].indexOf('base64') >= 0)
//             byteString = atob(dataURI.split(',')[1]);
//         else
//             byteString = unescape(dataURI.split(',')[1]);
//
//         // separate out the mime component
//         var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
//
//         // write the bytes of the string to a typed array
//         var ia = new Uint8Array(byteString.length);
//         for (var i = 0; i < byteString.length; i++) {
//             ia[i] = byteString.charCodeAt(i);
//         }
//
//         return new Blob([ia], {type:mimeString});
//     }
//
//     timer = setInterval(function () {
//         ctx.drawImage(video, 0, 0, 320, 240);
//         var data = canvas.toDataURL('image/jpeg', 1.0);
//         newblob = dataURItoBlob(data);
//         ws.send(newblob);
//     }, 250);
// }
