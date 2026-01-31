const getElement = (id) => document.getElementById(id);

// 1. Load available models
async function loadModels(apiKey) {
    if (!apiKey) return;
    
    const select = getElement('modelSelect');
    try {
        const response = await fetch('http://localhost:8000/models', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey })
        });
        const data = await response.json();
        
        if (data.models) {
            select.innerHTML = ''; // Clear existing
            data.models.forEach(model => {
                const opt = document.createElement('option');
                opt.value = model;
                opt.textContent = model;
                select.appendChild(opt);
            });
        }
    } catch (e) {
        console.error("Failed to load models:", e);
    }
}

// 2. Analyze Action
getElement('analyzeBtn').addEventListener('click', async () => {
    const apiKey = getElement('apiKey').value;
    const model = getElement('modelSelect').value;
    const resultDiv = getElement('result');
    const spinner = getElement('spinner');
    const btn = getElement('analyzeBtn');

    if (!apiKey) {
        alert('Please enter your Gemini API Key');
        return;
    }

    btn.disabled = true;
    spinner.style.display = 'block';
    resultDiv.textContent = '';

    try {
        // Fix: Use lastFocusedWindow for Side Panel context
        const tabs = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
        const tab = tabs[0];
        
        if (!tab || !tab.url) {
            throw new Error("Could not get current tab URL. Ensure a webpage is active.");
        }

        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: tab.url,
                api_key: apiKey,
                model: model
            })
        });

        const data = await response.json();
        
        if (data.analysis) {
            // Render Markdown
            resultDiv.innerHTML = marked.parse(data.analysis);
        } else {
            resultDiv.innerHTML = `<span style="color:red">Error: ${data.detail || JSON.stringify(data)}</span>`;
        }

    } catch (err) {
        resultDiv.textContent = "Error: " + err.message + "\n\nIs 'uv run server.py' running?";
    } finally {
        btn.disabled = false;
        spinner.style.display = 'none';
    }
});

// 3. UI Events
const apiKeyInput = getElement('apiKey');

// Load saved key
const savedKey = localStorage.getItem('spoon_gemini_key');
if (savedKey) {
    apiKeyInput.value = savedKey;
    loadModels(savedKey); // Auto load models on init
}

// Save key and reload models on change
apiKeyInput.addEventListener('change', (e) => {
    const key = e.target.value;
    localStorage.setItem('spoon_gemini_key', key);
    loadModels(key);
});
