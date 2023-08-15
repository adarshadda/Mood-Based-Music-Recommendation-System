let mediaRecorder;
let recordedChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = function(event) {
                recordedChunks.push(event.data);
            };
            mediaRecorder.onstop = function() {
                const audioBlob = new Blob(recordedChunks, { type: 'audio/mp3' });

                // Create a download link to save the audio recording
                const downloadLink = document.createElement('a');
                downloadLink.href = URL.createObjectURL(audioBlob);
                downloadLink.download = 'recorded_audio.mp3';
                downloadLink.click();

                // Reset the recordedChunks for the next recording
                recordedChunks = [];
            };
            mediaRecorder.start();
            document.getElementById("recordBtn").disabled = true;
            document.getElementById("stopBtn").disabled = false;
        })
        .catch(function(err) {
            console.log("Error accessing microphone:", err);
        });
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById("recordBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;
}

