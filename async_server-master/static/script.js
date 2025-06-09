async function downloadData() {
    document.getElementById("status").innerText = 
    "Connecting to service...";

    // Simulate delay before next step
    await new Promise(r => setTimeout(r, 500));
    document.getElementById("status").innerText = 
    "Getting data...";

    const response = await fetch("/download", {
        method: "POST",
    });

    const data = await response.json();

    document.getElementById("status").innerText = 
    "Operation complete.";
    document.getElementById("result").innerHTML = 
    data.result;
}
