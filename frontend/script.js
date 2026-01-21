async function runGenerator() {
    const prompt = document.getElementById('userPrompt').value;
    const btn = document.getElementById('genBtn');
    const outputArea = document.getElementById('outputArea');
    const resultImg = document.getElementById('resultImg');

    if (!prompt) {
        alert("Please describe your imagination first!");
        return;
    }

    // UI Feedback: Disable button and show loading state
    btn.disabled = true;
    btn.innerText = "Processing Magic...";

    try {
        // We call our FastAPI endpoint
        const response = await fetch(`http://127.0.0.1:8000/generate?prompt=${encodeURIComponent(prompt)}`);
        
        if (!response.ok) throw new Error("Backend is offline");

        // Convert the raw image bytes into a viewable URL
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        
        resultImg.src = imageUrl;
        outputArea.classList.remove('hidden');
    } catch (error) {
        console.error("Error:", error);
        alert("Make sure your Python backend is running on port 8000!");
    } finally {
        btn.disabled = false;
        btn.innerText = "Generate Image";
    }
}