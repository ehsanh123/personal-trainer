async function sendMessage() {
    const inputEl = document.getElementById("userInput");
    const statusEl = document.getElementById("status");
    const replyEl = document.getElementById("botReply");

    const message = inputEl.value.trim();
    if (!message) return;

    // Update status
    statusEl.innerText = "Connecting to service...";
    await delay(300);

    statusEl.innerText = "Getting data...";
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    statusEl.innerText = "Operation complete.";
    replyEl.innerText = data.reply;
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
