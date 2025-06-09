// Image upload and processing script


// Function to send a message to the server and get a response        
        
async function sendMessage() {
    const inputEl = document.getElementById("userInput");
    const statusEl = document.getElementById("status");
    const replyEl = document.getElementById("botReply");

    const message = inputEl.value.trim();
    if (!message) return;

    statusEl.innerText = "Getting data...";
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    statusEl.innerText = "Idle";
    replyEl.innerText = data.reply;
}


// Function to record voice and transcribe it

async function record_voice() {
    const massage_text = document.getElementById("userInput");
    const record_stat = document.getElementById("status_recording");
    const btn_text = document.getElementById("btn1");
                
    //////////////////////////give recordin command
    
    const response = await fetch("/start-recording", {
        method: "POST"
    });
    const data = await response.json();  // assuming you're returning JSON

    ////////////////////////if recording is not done
    
    if (data.message != "Recording Done") {
        btn_text.innerText = "Stop Recording";
        record_stat.innerText = "Recording...";
        return;
        }

    //////////////////////if recording is done
    ///////transcribe the audio
    record_stat.innerText = "Trascribint the audio...";
    btn_text.innerText = "Start Recording";

    const r2 = await fetch("/start-transcribe", { method: "POST" });
    
    const data2  = await r2.json(); 
    
    ////display the transcribed text

    record_stat.innerText = "Idle";

    massage_text.value = data2.input_text

    // record_stat.innerText = data.message;
}
