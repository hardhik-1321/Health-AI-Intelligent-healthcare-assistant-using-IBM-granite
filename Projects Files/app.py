from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI()

API_KEY = "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"
API_URL = "https://huggingface.co/ibm-granite/granite-3b-3.3b-instruct"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Healthcare AI Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #4a6fa5;
            --secondary: #6b8cae;
            --accent: #ff7e5f;
            --light: #f8f9fa;
            --dark: #212529;
            --success: #28a745;
            --info: #17a2b8;
            --warning: #ffc107;
            --danger: #dc3545;
        }

        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            background: var(--light);
            color: var(--dark);
            transition: all 0.3s ease;
            line-height: 1.6;
        }

        body.dark {
            background: #121212;
            color: #f0f0f0;
        }

        header {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 2.5rem 1rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: "";
            position: absolute;
            top: -50px;
            left: -50px;
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
        }

        header::after {
            content: "";
            position: absolute;
            bottom: -30px;
            right: -30px;
            width: 150px;
            height: 150px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 50%;
        }

        h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }

        header p {
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        main {
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }

        section {
            margin-bottom: 3rem;
            animation: fadeIn 0.5s ease forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 {
            color: var(--primary);
            font-size: 1.8rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .chatbox {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }

        body.dark .chatbox {
            background: #1e1e1e;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        }

        .chatbox:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
        }

        .chatlog {
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 1.5rem;
            padding: 0.5rem;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.02);
        }

        body.dark .chatlog {
            background: rgba(255, 255, 255, 0.05);
        }

        .bubble {
            margin: 10px 0;
            padding: 12px 16px;
            border-radius: 16px;
            max-width: 80%;
            line-height: 1.5;
            white-space: pre-wrap;
            position: relative;
            animation: bubbleIn 0.3s ease forwards;
            opacity: 0;
        }

        @keyframes bubbleIn {
            to { opacity: 1; }
        }

        .user {
            background: var(--primary);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }

        .bot {
            background: #e9f5ff;
            color: var(--dark);
            margin-right: auto;
            border-bottom-left-radius: 4px;
        }

        body.dark .user {
            background: var(--accent);
        }

        body.dark .bot {
            background: #2a2a2a;
            color: #f0f0f0;
        }

        form {
            display: flex;
            gap: 10px;
            margin-top: 1rem;
        }

        input[type="text"] {
            flex: 1;
            padding: 0.8rem 1rem;
            border-radius: 25px;
            border: 1px solid #ddd;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: rgba(0, 0, 0, 0.02);
        }

        body.dark input[type="text"] {
            background: rgba(255, 255, 255, 0.05);
            border-color: #444;
            color: #f0f0f0;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(74, 111, 165, 0.2);
        }

        button {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8rem 1.8rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(74, 111, 165, 0.3);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(74, 111, 165, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        footer {
            text-align: center;
            font-size: 0.9rem;
            color: #666;
            margin: 3rem auto;
            padding: 1rem;
            border-top: 1px solid #eee;
        }

        body.dark footer {
            color: #888;
            border-top-color: #333;
        }

        .toggle-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 100;
        }

        .toggle {
            width: 60px;
            height: 30px;
            background: #ddd;
            display: inline-block;
            border-radius: 30px;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
        }

        .toggle::after {
            content: "";
            width: 26px;
            height: 26px;
            background: white;
            border-radius: 50%;
            position: absolute;
            top: 2px;
            left: 2px;
            transition: 0.3s;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        input:checked + .toggle {
            background: var(--primary);
        }

        input:checked + .toggle::after {
            transform: translateX(30px);
        }

        input[type="checkbox"] {
            display: none;
        }

        ul {
            padding-left: 1.5rem;
            list-style-type: none;
        }

        ul li {
            margin-bottom: 0.5rem;
            position: relative;
            padding-left: 1.5rem;
        }

        ul li::before {
            content: "•";
            color: var(--accent);
            font-size: 1.5rem;
            position: absolute;
            left: 0;
            top: -2px;
        }

        .feature-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }

        .feature-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }

        body.dark .feature-card {
            background: #1e1e1e;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        .feature-card i {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }

        .feature-card h3 {
            margin: 0.5rem 0;
            color: var(--primary);
        }

        .typing-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: var(--primary);
            border-radius: 50%;
            margin-right: 4px;
            opacity: 0.4;
            animation: typing 1.4s infinite both;
        }

        .typing-indicator:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-indicator:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 100% { opacity: 0.4; transform: translateY(0); }
            50% { opacity: 1; transform: translateY(-5px); }
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            main {
                padding: 0 1rem;
            }
            
            .feature-cards {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body class="light">
    <div class="toggle-container">
        <input type="checkbox" id="modeToggle">
        <label for="modeToggle" class="toggle"></label>
    </div>

    <header>
        <h1><i class="fas fa-heartbeat"></i> Healthcare AI Assistant</h1>
        <p>Your intelligent, private health companion powered by AI</p>
    </header>

    <main>
        <section>
            <h2><i class="fas fa-info-circle"></i> About This Assistant</h2>
            <p>
                Our Healthcare AI Assistant provides intelligent health guidance powered by artificial intelligence.
                It offers symptom analysis and natural remedy suggestions while maintaining complete privacy.
            </p>
            
            <div class="feature-cards">
                <div class="feature-card">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Privacy First</h3>
                    <p>All your health queries remain confidential and secure.</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-brain"></i>
                    <h3>AI-Powered</h3>
                    <p>Powered by advanced AI models for accurate health insights.</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-leaf"></i>
                    <h3>Natural Solutions</h3>
                    <p>Get home remedy suggestions based on natural ingredients.</p>
                </div>
            </div>
        </section>

        <section>
            <h2><i class="fas fa-stethoscope"></i> Symptom Checker</h2>
            <p>Describe your symptoms and receive potential condition insights.</p>
            <div class="chatbox">
                <div class="chatlog" id="symptom-log"></div>
                <form onsubmit="sendChat(event, 'symptom')">
                    <input type="text" id="symptom-input" placeholder="e.g., headache, fever, fatigue...">
                    <button type="submit"><i class="fas fa-search"></i> Analyze</button>
                </form>
            </div>
        </section>

        <section>
            <h2><i class="fas fa-mortar-pestle"></i> Remedy Advisor</h2>
            <p>Enter a known condition to receive natural treatment suggestions.</p>
            <div class="chatbox">
                <div class="chatlog" id="remedy-log"></div>
                <form onsubmit="sendChat(event, 'remedy')">
                    <input type="text" id="remedy-input" placeholder="e.g., migraine, cold, indigestion...">
                    <button type="submit"><i class="fas fa-lightbulb"></i> Suggest</button>
                </form>
            </div>
        </section>

        <section>
            <h2><i class="fas fa-cogs"></i> How It Works</h2>
            <ul>
                <li>You describe symptoms or enter a known condition</li>
                <li>Our AI processes your input using advanced models</li>
                <li>You receive personalized health insights and suggestions</li>
                <li>All interactions are secure and private</li>
            </ul>
        </section>
    </main>

    <footer>
        <p><i class="fas fa-exclamation-circle"></i> Important: This tool provides educational information only and is not a substitute for professional medical advice.</p>
        <p>© 2023 Healthcare AI Assistant | Powered by AI</p>
    </footer>

    <script>
        // Dark mode toggle
        document.getElementById("modeToggle").addEventListener("change", () => {
            document.body.classList.toggle("dark");
            localStorage.setItem('darkMode', document.body.classList.contains('dark'));
        });

        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark');
            document.getElementById('modeToggle').checked = true;
        }

        async function sendChat(event, type) {
            event.preventDefault();
            const input = document.getElementById(type + "-input");
            const log = document.getElementById(type + "-log");
            const msg = input.value.trim();
            if (!msg) return;

            appendMessage(log, "user", msg);
            input.value = "";

            const responseBubble = appendMessage(log, "bot", '<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span>');

            const prompt = type === "symptom"
                ? `Symptoms: ${msg}\nWhat disease could it indicate? Provide potential conditions and when to see a doctor.`
                : `Disease: ${msg}\nSuggest natural home remedies and lifestyle changes.`;

            try {
                const res = await fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: `message=${encodeURIComponent(prompt)}`
                });

                const data = await res.json();
                responseBubble.innerHTML = data.response;
            } catch (error) {
                responseBubble.textContent = "Sorry, there was an error processing your request. Please try again.";
            }
        }

        function appendMessage(container, role, text) {
            const p = document.createElement("p");
            p.className = "bubble " + role;
            if (typeof text === 'string') {
                p.innerHTML = text;
            } else {
                p.textContent = text;
            }
            container.appendChild(p);
            container.scrollTop = container.scrollHeight;
            return p;
        }
    </script>
</body>
</html>

"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=HTML)

@app.post("/ask")
async def ask(message: str = Form(...)):
    payload = {
        "model": "ibm-granite/granite-3.3-2b-instruct ",
        "messages": [
            {"role": "system", "content": "You are a smart, safe, and ethical healthcare assistant. Help the user understand possible diseases from symptoms, or suggest natural remedies for diseases."},
            {"role": "user", "content": message}
        ]
    }
    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        output = res.json()["choices"][0]["message"]["content"]
        return JSONResponse(content={"response": output})
    except Exception as e:
        return JSONResponse(content={"response": f"Error: {str(e)}"})
