let livePoseRunning = false;

function startLivePose() {
    livePoseRunning = true;
    document.getElementById("poseStatus").innerText = "Status: Live";

    const video = document.getElementById('video');
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = 400;
    tempCanvas.height = 300;

    async function loop() {
        if (!livePoseRunning) return;

        // Grab frame directly to temp canvas (NOT shown)
        tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
        const imageData = tempCanvas.toDataURL('image/png');

        await uploadAndDisplayPose(imageData);

        setTimeout(() => {
            requestAnimationFrame(loop);
        }, 100); // ~10 FPS
    }

    loop();
}

function stopLivePose() {
    livePoseRunning = false;
    document.getElementById("poseStatus").innerText = "Status: Stopped";
}

async function uploadAndDisplayPose(imageData) {
    const canvas = document.getElementById("image1");
    const ctx = canvas.getContext("2d");

    try {
        const response = await fetch("/upload-photo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: imageData ,"name":"3"})
        });

        const result = await response.json();
        // const img = new Image();
        // img.onload = () => {
        //     ctx.clearRect(0, 0, canvas.width, canvas.height);
        //     ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        // };
        // img.src = result.processed_image;
        const statusEl = document.getElementById("poseStatus");
        let text = "Status:\n";
        for (const [key, value] of Object.entries(result.angles)) {
            text += `${key}: ${value}\n`;
        }
        statusEl.innerText = text;


    } catch (err) {
        console.error("Pose detection failed:", err);
        document.getElementById("poseStatus").innerText = "Status: Error";
    }
}
