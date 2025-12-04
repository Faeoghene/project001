// Change this depending on which backend you're running:
const API_URL = "http://localhost:8000/";   // FastAPI

const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const uploadLabel = document.getElementById("uploadLabel");
const statusText = document.getElementById("status");
const outputBox = document.getElementById("output");

uploadArea.addEventListener("click", () => fileInput.click());


fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    uploadLabel.textContent = `Selected: ${file.name}`;
    statusText.textContent = "Processing...";
    outputBox.value = "";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || error.error || "Unknown error");
        }

        const data = await res.json();
        statusText.textContent = "Done!";
        outputBox.value = data.text || "";

    } catch (err) {
        statusText.textContent = "Error: " + err.message;
    }
});
