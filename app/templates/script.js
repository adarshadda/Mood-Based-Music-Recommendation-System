<script>
        let mediaRecorder;
        let recordedChunks = [];

        function startRecording() {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.ondataavailable = function (event) {
                        recordedChunks.push(event.data);
                    };
                    mediaRecorder.onstop = function () {
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
                    document.getElementById("startBtn").disabled = true;
                    document.getElementById("stopBtn").disabled = false;

                    // Pause the audio prompt while recording
                    const audioPrompt = document.getElementById("audioPrompt");
                    audioPrompt.pause();

                    // Initialize the frequency graph
                    initializeFrequencyGraph(stream);
                })
                .catch(function (err) {
                    console.log("Error accessing microphone:", err);
                });
        }

        function stopRecording() {
            mediaRecorder.stop();
            document.getElementById("startBtn").disabled = false;
            document.getElementById("stopBtn").disabled = true;

            // Resume the audio prompt after recording
            const audioPrompt = document.getElementById("audioPrompt");
            audioPrompt.play();

            // Clear the frequency graph when recording stops
            const canvas = document.getElementById("frequencyGraph");
            const canvasCtx = canvas.getContext("2d");
            canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

            // Create a Blob from recordedChunks
            const audioBlob = new Blob(recordedChunks, { type: 'audio/mp3' });

            // Create a FormData object to send the audio data to the server
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recorded_audio.mp3');

            // Make an HTTP POST request to your Flask server to save the audio in the "temp" directory
            fetch('/save_audio', {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the response from your Flask server as needed
                console.log('Response from server:', data);

                // Example: Display the predicted emotion in your web page
                const emotionElement = document.getElementById("emotion");
                emotionElement.textContent = `Predicted Emotion: ${data.emotion}`;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });

            // Reset the recordedChunks for the next recording
            recordedChunks = [];
        }


        function initializeFrequencyGraph(stream) {
            // Create an AudioContext and connect the microphone stream to it
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const mediaStreamSource = audioContext.createMediaStreamSource(stream);

            // Create an AnalyserNode to analyze the frequency data
            const analyserNode = audioContext.createAnalyser();
            analyserNode.fftSize = 256;
            const bufferLength = analyserNode.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);

            // Connect the AnalyserNode to the microphone stream
            mediaStreamSource.connect(analyserNode);

            // Create the frequency graph
            const canvas = document.getElementById("frequencyGraph");
            const canvasCtx = canvas.getContext("2d");

            function updateFrequencyGraph() {
                analyserNode.getByteFrequencyData(dataArray);

                canvasCtx.fillStyle = 'rgb(200, 200, 200)';
                canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

                const barWidth = (canvas.width / bufferLength) * 2;
                let x = 0;
                for (let i = 0; i < bufferLength; i++) {
                    const barHeight = dataArray[i] / 2;
                    canvasCtx.fillStyle = 'rgb(' + (barHeight + 100) + ',50,50)';
                    canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
                    x += barWidth + 1;
                }

                requestAnimationFrame(updateFrequencyGraph);
            }

            // Start updating the frequency graph
            updateFrequencyGraph();
        }
    </script>