from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- TOGETHER AI CONFIGURATION ---
client = OpenAI(
    api_key="tgp_v1_HJ-DBGmpB11P6FWn7uW5Tev6OssHYnEaR1cAZhlVTeI",
    base_url="https://api.together.xyz/v1"
)

# --- FUTURISTIC RING HUD ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MARK 97</title>
    <style>
        body { background: #000; color: #00d2ff; font-family: 'Segoe UI', sans-serif; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .ring-container { position: relative; width: 280px; height: 280px; display: flex; justify-content: center; align-items: center; }
        .ring { position: absolute; border: 2px solid #00d2ff; border-radius: 50%; animation: pulse 1.5s infinite ease-in-out; }
        .r1 { width: 100%; height: 100%; opacity: 0.2; }
        .r2 { width: 75%; height: 75%; opacity: 0.5; animation-delay: 0.3s; }
        .r3 { width: 45%; height: 45%; opacity: 1; border-width: 4px; box-shadow: 0 0 30px #00d2ff; }
        @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 0.4; } 50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 50px #00d2ff; } }
        .content { position: absolute; z-index: 10; text-align: center; }
        h1 { letter-spacing: 12px; font-weight: bold; text-shadow: 0 0 15px #00d2ff; margin-bottom: 40px; color: #00d2ff; }
        #chat-box { height: 70px; font-size: 16px; margin-bottom: 25px; color: #fff; font-style: italic; max-width: 400px; }
        input { background: rgba(0, 210, 255, 0.1); border: 1px solid #00d2ff; color: #00d2ff; padding: 12px; width: 250px; border-radius: 30px; text-align: center; outline: none; box-shadow: 0 0 10px #00d2ff33; }
    </style>
</head>
<body>
    <div class="ring-container"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div></div>
    <div class="content">
        <h1>J.A.R.V.I.S.</h1>
        <div id="chat-box">SYSTEMS LIVE. AWAITING COMMAND, SIR.</div>
        <input type="text" id="userInput" placeholder="COMMAND ARSLAN ZAHEER..." onkeypress="if(event.key==='Enter') ask()">
    </div>
    <script>
        async function ask() {
            let input = document.getElementById('userInput');
            let box = document.getElementById('chat-box');
            if(!input.value) return;
            box.innerText = "ACCESSING NEURAL NETWORK...";
            let userVal = input.value;
            input.value = '';
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(userVal));
                let data = await res.json();
                box.innerText = data.reply;
                let s = new SpeechSynthesisUtterance(data.reply);
                s.lang = 'en-GB';
                window.speechSynthesis.speak(s);
            } catch(e) { box.innerText = "COMMUNICATION LINK SEVERED, SIR."; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_UI)

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "Your name is JARVIS. You were created by Arslan Zaheer. You are his loyal AI. Answer briefly and call him Sir."},
                {"role": "user", "content": msg}
            ]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except: return jsonify({"reply": "Sir, I encountered a neural bridge error."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
