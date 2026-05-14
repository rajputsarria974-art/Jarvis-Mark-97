from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- CONFIGURATION ---
client = OpenAI(
    api_key="tgp_v1_HJ-DBGmpB11P6FWn7uW5Tev6OssHYnEaR1cAZhlVTeI",
    base_url="https://api.together.xyz/v1"
)

# --- FUTURISTIC HUD INTERFACE ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS MARK 97</title>
    <style>
        body { background: #000; color: #00d2ff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px; overflow-x: hidden; }
        .hud-container { border: 2px solid #00d2ff; border-radius: 20px; padding: 25px; max-width: 500px; margin: auto; box-shadow: 0 0 30px #00d2ff33; background: rgba(0, 20, 30, 0.5); }
        h2 { letter-spacing: 5px; text-shadow: 0 0 10px #00d2ff; font-weight: 300; }
        #chat-box { height: 350px; overflow-y: auto; text-align: left; margin-bottom: 20px; border-bottom: 1px solid #1a3a4a; padding: 10px; scroll-behavior: smooth; }
        .user-msg { color: #00d2ff; margin: 10px 0; font-weight: bold; }
        .jarvis-msg { color: #ffffff; margin: 10px 0; border-left: 2px solid #00d2ff; padding-left: 10px; font-style: italic; }
        .input-area { display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; background: #051015; border: 1px solid #00d2ff; color: #fff; border-radius: 5px; outline: none; }
        button { padding: 12px 25px; background: #00d2ff; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; color: #000; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .status-bar { font-size: 10px; margin-top: 15px; color: #004a5a; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="hud-container">
        <h2>JARVIS <span style="font-size: 15px;">MARK 97</span></h2>
        <div id="chat-box">
            <div class="jarvis-msg">Systems online. All circuits functional. Standing by for Arslan Zaheer's command.</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Waiting for command, Sir..." onkeypress="if(event.key==='Enter') ask()">
            <button onclick="ask()">SEND</button>
        </div>
        <div class="status-bar">LLAMA-3.1 CORE // CREATED BY ARSLAN ZAHEER // SECURE CONNECTION</div>
    </div>

    <script>
        async function ask() {
            let inputField = document.getElementById('userInput');
            let userText = inputField.value.trim();
            if(!userText) return;

            let chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="user-msg">SIR: ${userText}</div>`;
            inputField.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                let response = await fetch('/chat?msg=' + encodeURIComponent(userText));
                let data = await response.json();
                
                chatBox.innerHTML += `<div class="jarvis-msg">JARVIS: ${data.reply}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;

                let speech = new SpeechSynthesisUtterance(data.reply);
                speech.lang = 'en-GB';
                speech.rate = 1.1;
                window.speechSynthesis.speak(speech);

            } catch (error) {
                chatBox.innerHTML += `<div class="jarvis-msg" style="color:red;">Sir, communication link disrupted.</div>`;
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
    user_msg = request.args.get('msg')
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Your name is JARVIS. You were created and programmed by the brilliant Arslan Zaheer. You are his loyal personal AI assistant. If anyone asks who made you, proudly say 'I was created by Arslan Zaheer'. Always address him as Sir and maintain a witty, helpful, and futuristic tone."
                },
                {"role": "user", "content": user_msg}
            ]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Sir, I've encountered a neural bridge error."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
