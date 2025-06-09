///////////////////////
async function loadImageFromButton() {
    const inputEl = document.getElementById("uploadStatus");
    inputEl.innerText = "Loading image...";

    const fileInput = document.getElementById("imageLoader");

    return new Promise((resolve) => {
        fileInput.onchange = function () {
            const file = fileInput.files[0];

            if (!file) {
                inputEl.innerText = "No file selected";
                resolve(null);
                return;
            }

            inputEl.innerText = "File found";

            // Optionally load image into canvas
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = new Image();
                img.onload = function () {
                    const canvas = document.getElementById("image1");
                    const ctx = canvas.getContext("2d");
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);

            resolve(file);
        };

        // Trigger file picker
        fileInput.click();
    });
}

////////
async function uploadCanvasImage() {
    const canvas = document.getElementById("image1");
    const statusEl = document.getElementById("uploadStatus");

    statusEl.innerText = "Status: Preparing image...";

    // Convert canvas image to base64
    const imageData = canvas.toDataURL("image/png");

    statusEl.innerText = "Status: Sending image to server...";

    // Send image to backend
    try {
        const response = await fetch("/upload-photo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: imageData })
        });

        statusEl.innerText = "Status: Waiting for response...";

        const result = await response.json();
        const processedImage = result.processed_image;

        // Load returned image into canvas
        const img = new Image();
        img.onload = function () {
            const ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            statusEl.innerText = "Status: Done ✅";
        };
        img.src = processedImage;
    } catch (error) {
        console.error("Upload error:", error);
        statusEl.innerText = "Status: Failed ❌";
    }
}
