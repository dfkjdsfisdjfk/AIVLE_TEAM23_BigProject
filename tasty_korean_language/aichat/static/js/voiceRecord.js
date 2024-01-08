$(document).ready(function(){
    let isRecording = false;

    if (navigator.mediaDevices){
        let recordArray = []; // 녹음 데이터 저장 변수

        navigator.mediaDevices.getUserMedia({audio: true})
        .then((stream) => {
            const mediaRecorder = new MediaRecorder(stream);

            // 녹음 버튼 클릭했을 때
            $('#record').on('click', function(){
                if (!isRecording){
                    mediaRecorder.start();
                    $(this).addClass('recording');
                }
                else {
                    mediaRecorder.stop();
                    $(this).removeClass('recording');
                }
                isRecording = !isRecording;
            });

            mediaRecorder.onstop = (event) => {
                const blob = new Blob(recordArray, {
                    type: 'audio/mp3'
                });
                recordArray = [];

                const formData = new FormData($('#chat-form')[0]);
                // const formData = new FormData();
                // formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());
                formData.append('audio_file', blob, 'recorded_audio.mp3');
                // formData.append('message', $('#text-input').val());

                // 서버로 FormData 전송
                $.ajax({
                    url: $('#chat-form').attr('action'),
                    // action: $('#chat-form').attr('action'),
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    enctype: 'multipart/form-data',
                    success: function(response) {
                        // Handle success if needed
                    },
                    error: function(error) {
                        // Handle error if needed
                    }
                });
            };

            // 녹음 데이터 배열에 저장
            mediaRecorder.ondataavailable = (event) => {
                recordArray.push(event.data);
            };
        })
        .catch((err) => {
            console.log(err);
            alert(err);
        })
    }
});






// $(document).ready(function(){
//     let isRecording = false;

//     if (navigator.mediaDevices){
//         let recordArray = []; // 녹음 데이터 저장 변수

//         navigator.mediaDevices.getUserMedia({audio: true})
//         .then((stream) => {
//             const mediaRecorder = new MediaRecorder(stream);

//             // 녹음 버튼 클릭했을 때
//             $('#record').on('click', function(){
//                 if (!isRecording){
//                     mediaRecorder.start();
//                     $(this).addClass('recording');
//                     // isRecording = true;
//                 }
//                 else {
//                     mediaRecorder.stop();
//                     $(this).removeClass('recording');
//                     // isRecording = false;
//                 }
//                 isRecording = !isRecording;
//             });

//             mediaRecorder.onstop = (event) => {

//                 // 녹음 데이터 audio 태그 추가
//                 var $audio = $('<audio controls>');
//                 $('#chat-box').append($('<article class="user-chat">').append($audio));

//                 // const blob = new Blob(recordArray, {
//                 //     'type': 'audio/mp3; codecs=opus'
//                 // });
//                 const blob = new Blob(recordArray, {
//                     type: 'audio/mp3'
//                 });
//                 recordArray = [];

//                 const audioURL = URL.createObjectURL(blob);
//                 $audio.attr('src', audioURL);

//                 // form 데이터 post로 전송
//                 const formData = new FormData($('#chat-form')[0]);
//                 document.getElementById('audio-input').value = blob;

//                 formData.append('audio_file', blob, 'recorded_audio.mp3');
//                 // $.ajax({
//                 //     url: $('#chat-form').attr('action'),
//                 //     type: 'POST',
//                 //     data: formData,
//                 //     processData: false,
//                 //     contentType: false,
//                 //     success: function(response) {
//                 //         // Handle success if needed
//                 //     },
//                 //     error: function(error) {
//                 //         // Handle error if needed
//                 //     }
//                 // });

//                 // 녹음 파일 저장
//                 // const formData = new FormData($('#chat-form')[0]);
//                 // formData.append('audio_file', blob, 'recorded_audio.mp3');
//                 // $.ajax({
//                 //     url: $('#chat-form').attr('action'),
//                 //     type: 'POST',
//                 //     data: formData,
//                 //     processData: false,
//                 //     contentType: false,
//                 //     success: function(response) {
//                 //         // Handle success if needed
//                 //     },
//                 //     error: function(error) {
//                 //         // Handle error if needed
//                 //     }
//                 // });

//                 // // 녹음 파일 저장
//                 // const a = document.createElement('a');
//                 // a.href = audioURL;
//                 // a.download = "record" + Date.now();
//                 // a.click();
//             };

//             // 녹음 데이터 배열에 저장
//             mediaRecorder.ondataavailable = (event) => {
//                 recordArray.push(event.data);
//             };

//         })
//         .catch((err) => {
//             console.log(err);
//             alert(err);
//         })
//     }
    
// });