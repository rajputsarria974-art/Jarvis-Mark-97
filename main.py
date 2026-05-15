import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- ARSLAN INDUSTRIES CONFIG ---
# GitHub Codespaces mein hum key direct define kar rahe hain taake error na aaye
SAMBA_KEY = "91799786-896c-4813-8207-68b323c21a11"

HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>J.A.R.V.I.S | ARSLAN INDUSTRIES</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
        
        body { 
            background: radial-gradient(circle, #051923 0%, #00050a 100%);
            color: #00d2ff; font-family: 'Orbitron', sans-serif; 
            margin: 0; overflow: hidden; height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }

        .header { position: absolute; top: 50px; text-align: center; }
        .logo { 
            font-size: 60px; font-weight: 900; letter-spacing: 20px; color: #fff;
            text-shadow: 0 0 20px #00d2ff, 0 0 40px #00d2ff;
        }
        .sub { font-size: 10px; letter-spacing: 5px; color: rgba(0, 210, 255, 0.6); margin-top: 10px; }

        .hud-main {
            position: relative; width: 300px; height: 300px;
            display: flex; align-items: center; justify-content: center;
        }

        .ring {
            position: absolute; width: 100%; height: 100%;
            border: 2px solid rgba(0, 210, 255, 0.2); border-radius: 50%;
        }

        .ring-spin {
            position: absolute; width: 90%; height: 90%;
            border: 4px dashed #00d2ff; border-radius: 50%;
            animation: spin 12s linear infinite; opacity: 0.6;
        }

        .core-glow {
            width: 80px; height: 80px; background: radial-gradient(circle, #fff, #00d2ff);
            border-radius: 50%; box-shadow: 0 0 60px #00d2ff;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes spin { 100% { transform: rotate(360deg); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); opacity: 0.7; } }

        #response-box {
            width: 80%; max-width: 700px; margin-top: 40px; padding: 20px;
            background: rgba(0, 210, 255, 0.05); border-left: 4px solid #00d2ff;
            min-height: 40px; color: #fff; font-size: 18px; text-transform: uppercase;
        }

        .input-container { position: fixed; bottom: 80px; width: 100%; text-align: center; }
        input {
            background: rgba(0, 0, 0, 0.8); border: 1px solid #00d2ff; color: #00d2ff;
            padding: 15px 30px; width: 400px; border-radius: 50px; outline: none;
            font-family: 'Orbitron'; font-size: 16px; box-shadow: 0 0 15px rgba(0,210,255,0.2);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">J.A.R.V.I.S</div>
        <div class="sub">VIRTUAL ASSISTANT | ARSLAN INDUSTRIES</div>
    </div>

    <div class="hud-main">
        <div class="ring"></div>
        <div class="ring-spin"></div>
        <div class="core-glow"></div>
    </div>

    <div id="response-box">SYSTEM INITIALIZED, SIR ARSLAN.</div>

    <div class="input-container">
        <input type="text" id="user-in" placeholder="AWAITING COMMAND..." onkeypress="if(event.key==='Enter') send()">
    </div>

    <script>
        async function send() {
            const i = document.getElementById('user-in');
            const r = document.getElementById('response-box');
            if(!i.value) return;
            
            let cmd = i.value;
            i.value = '';
            r.innerText = ">> ANALYZING DATA...";
            
            try {
                const res = await fetch('/chat?msg=' + encodeURIComponent(cmd));
                const data = await res.json();
                r.innerText = ">> " + data.reply;
                
                // Voice Response
                const speech = new SpeechSynthesisUtterance(data.reply);
                speech.rate = 1.1;
                window.speechSynthesis.speak(speech);
            } catch(e) {
                r.innerText = ">> ERROR: NEURAL LINK DISCONNECTED.";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    url = "https://api.sambanova.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {SAMBA_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Meta-Llama-3.1-70B-Instruct",
        "messages": [
            {"role": "system", "content": "You are J.A.R.V.I.S, the highly intelligent and polite AI of Sir Arslan Zaheer. Use short, sharp, and professional phrases. Always call him Sir."},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.1
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        bot_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})
    except:
        return jsonify({"reply": "Sir, there is a connection issue with SambaNova servers."})

if __name__ == "__main__":
    # GitHub Codespaces usually uses port 8080 or 5000
    app.run(host='0.0.0.0', port=8080)
