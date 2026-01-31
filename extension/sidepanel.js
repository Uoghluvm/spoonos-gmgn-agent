document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const apiKey = document.getElementById("apiKey").value;
  const model = document.getElementById("modelSelect").value;
  const resultDiv = document.getElementById("result");
  const spinner = document.getElementById("spinner");
  const btn = document.getElementById("analyzeBtn");

  if (!apiKey) {
    alert("Please enter your Gemini API Key");
    return;
  }

  // UI Loading State
  btn.disabled = true;
  spinner.style.display = "block";
  resultDiv.textContent = "";

  try {
    // Get current tab URL
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    if (!tab || !tab.url) {
      throw new Error("Could not get current tab URL");
    }

    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: tab.url,
        api_key: apiKey,
        model: model,
      }),
    });

    const data = await response.json();

    if (data.analysis) {
      resultDiv.textContent = data.analysis;
    } else {
      resultDiv.textContent = "Error: " + (data.detail || "Unknown error");
    }
  } catch (err) {
    resultDiv.textContent =
      "Failed to connect to Agent: " +
      err.message +
      "\n\nMake sure 'uv run server.py' is running!";
  } finally {
    btn.disabled = false;
    spinner.style.display = "none";
  }
});

// Auto-save API Key for convenience
document.getElementById("apiKey").value =
  localStorage.getItem("spoon_gemini_key") || "";
document.getElementById("apiKey").addEventListener("change", (e) => {
  localStorage.setItem("spoon_gemini_key", e.target.value);
});
