from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- SAMBANOVA CONFIGURATION ---
client = OpenAI(
    api_key="4469733d-9d41-4c6c-819a-9e6e8e8e7805", 
    base_url="https://api.sambanova.ai/v1"
)

# --- TONY STARK RING INTERFACE ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MARK 97</title>
    <style>
        body { background: #000; color: #00d2ff; font-family: 'Courier New', monospace; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .ring-container { position: relative; width: 250px; height: 250px; display: flex; justify-content: center; align-items: center; }
        .ring { position: absolute; border: 2px solid #00d2ff; border-radius: 50%; animation: pulse 1.5s infinite ease-in-out; }
        .r1 { width: 100%; height: 100%; opacity: 0.2; }
        .r2 { width: 70%; height: 70%; opacity: 0.5; animation-delay: 0.3s; }
        .r3 { width: 40%; height: 40%; opacity: 1; border-width: 3px; box-shadow: 0 0 20px #00d2ff; }
        @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 0.4; } 50% { transform: scale(1.15); opacity: 1; } }
        .content { position: absolute; z-index: 10; text-align: center; }
        h1 { letter-spacing: 8px; font-size: 20px; text-shadow: 0 0 10px #00d2ff; margin-bottom: 30px; }
        #chat-box { height: 80px; font-size: 16px; margin-bottom: 20px; max-width: 350px; color: #fff; font-weight: bold; overflow-y: auto; }
        input { background: none; border: 1px solid #00d2ff; color: #00d2ff; padding: 12px; width: 220px; border-radius: 5px; text-align: center; outline: none; }
    </style>
</head>
<body>
    <div class="ring-container"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div></div>
    <div class="content">
        <h1>J.A.R.V.I.S.</h1>
        <div id="chat-box">SAMBANOVA CORE ACTIVE. AWAITING SIR...</div>
        <input type="text" id="userInput" placeholder="COMMAND ARSLAN..." onkeypress="if(event.key==='Enter') ask()">
    </div>
    <script>
        async function ask() {
            let input = document.getElementById('userInput');
            let box = document.getElementById('chat-box');
            if(!input.value) return;
            box.innerText = "ACCESSING SAMBANOVA...";
            let userVal = input.value;
            input.value = '';
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(userVal));
                let data = await res.json();
                box.innerText = data.reply;
                let s = new SpeechSynthesisUtterance(data.reply);
                s.lang = 'en-GB';
                window.speechSynthesis.speak(s);
            } catch(e) {
                box.innerText = "COMMUNICATION LINK SEVERED, SIR.";
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
    try:
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-70B-Instruct",
            messages=[
                {"role": "system", "content": "You are JARVIS, a loyal AI created by Arslan Zaheer. Answer briefly and call him Sir."},
                {"role": "user", "content": msg}
            ]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Sir, SambaNova Error: {str(e)[:40]}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
