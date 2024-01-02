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
                    isRecording = true;
                }
                else {
                    mediaRecorder.stop();
                    $(this).removeClass('recording');
                    isRecording = false;
                }
            });

            mediaRecorder.onstop = (event) => {
                // 녹음 데이터 audio 태그 추가
                var $audio = $('<audio controls>');
                $('#chat-box').append($('<article class="user-chat">').append($audio));

                const blob = new Blob(recordArray, {
                    'type': 'audio/wav codecs=opus'
                });
                recordArray = [];

                const audioURL = URL.createObjectURL(blob);
                $audio.attr('src', audioURL);

                // 녹음 파일 저장
                // const a = document.createElement('a');
                // a.href = audioURL;
                // a.download = "record" + Date.now();
                // a.click();
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