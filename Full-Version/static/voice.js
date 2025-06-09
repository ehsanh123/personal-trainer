let mediaRecorder;
let recordedChunks = [];

const TARGET_SAMPLE_RATE = 44100; // e.g., 16000 Hz


async function startRecording() {
    // const massage_text = document.getElementById("userInput");
    const record_stat = document.getElementById("status_recording");
    // const btn_text = document.getElementById("btn1");

    recordedChunks = [];

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioContext = new AudioContext({ sampleRate: TARGET_SAMPLE_RATE });

    const source = audioContext.createMediaStreamSource(stream);
    const destination = audioContext.createMediaStreamDestination();
    source.connect(destination);

    mediaRecorder = new MediaRecorder(destination.stream);

    mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) recordedChunks.push(e.data);
    };

    // btn_text.innerText = "Stop Recording";
    record_stat.innerText = "Recording...";

    mediaRecorder.onstop = sendAudioToBackend;
    mediaRecorder.start();

    
    // console.log("Recording started with fixed sample rate:", TARGET_SAMPLE_RATE);
}

function stopRecording() {
    mediaRecorder.stop();
    console.log("Recording stopped");
}

async function sendAudioToBackend() {
    const massage_text = document.getElementById("userInput");
    const record_stat = document.getElementById("status_recording");
    // const btn_text = document.getElementById("btn1");

    record_stat.innerText = "Trascribing the audio...";
    // btn_text.innerText = "Start Recording";

    const blob = new Blob(recordedChunks, { type: "audio/webm" }); // Browser default
    const formData = new FormData();
    formData.append("file", blob, "recorded_audio.webm");

    try {
        const response = await fetch("/transcribe-audio", {
            method: "POST",
            body: formData
        });

    
        const result = await response.json();

        record_stat.innerText = "Idle";

        // console.log("Transcription result:", result);

        massage_text.value = result.input_text
        
        if (massage_text.value != "") //return;
            await sendMessage();
        

    } catch (error) {
        record_stat.innerText = "Error during transcription";
        // console.error("Error sending audio to backend:", error);
    }
}

// Function to send a message to the server and get a response        
        
async function sendMessage() {
    const inputEl = document.getElementById("userInput");
    const statusEl = document.getElementById("status");
    const replyEl = document.getElementById("botReply");

    const message = inputEl.value.trim();
    if (message) //return;
    {
    statusEl.innerText = "Getting data...";
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    statusEl.innerText = "Idle1";
    // replyEl.innerHTML = data.reply;

    let formattedReply = data.reply
    .replace(/\\n/g, '<br>')            
    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

    replyEl.innerHTML = formattedReply + '1';
    }

}