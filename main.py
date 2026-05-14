import os
from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- JARVIS CORE (SambaNova API) ---
API_KEY = "f0e41874-8132-4025-a179-13a0affac917"
client = OpenAI(api_key=API_KEY, base_url="https://api.sambanova.ai/v1")

# Futuristic UI Design
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS MARK 97</title>
    <style>
        body { background: #050505; color: #00d2ff; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        header { padding: 15px; border-bottom: 2px solid #00d2ff; box-shadow: 0 0 15px #00d2ff55; text-align: center; background: #000; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; background: radial-gradient(circle, #0a0a0a 0%, #000 100%); }
        .msg { max-width: 80%; padding: 12px 18px; border-radius: 20px; font-size: 15px; line-height: 1.5; }
        .user { align-self: flex-end; background: #00d2ff; color: #000; border-bottom-right-radius: 2px; box-shadow: 0 4px 10px rgba(0,210,255,0.3); }
        .jarvis { align-self: flex-start; background: rgba(255,255,255,0.05); border: 1px solid #00d2ff; border-bottom-left-radius: 2px; }
        .input-box { padding: 20px; background: #000; border-top: 1px solid #111; display: flex; gap: 10px; }
        input { flex: 1; padding: 12px 20px; background: #111; border: 1px solid #333; color: #fff; border-radius: 30px; outline: none; }
        input:focus { border-color: #00d2ff; }
        button { background: #00d2ff; border: none; padding: 10px 25px; border-radius: 30px; color: #000; font-weight: bold; cursor: pointer; }
        .status { font-size: 10px; color: #00d2ff; opacity: 0.6; margin-top: 5px; }
    </style>
</head>
<body>
    <header>
        <h2 style="margin:0; letter-spacing:3px;">JARVIS <span style="color:#fff">MARK 97</span></h2>
        <div class="status">SYSTEM: ONLINE | SECURE CONNECTION</div>
    </header>
    <div id="chat"></div>
    <div class="input-box">
        <input type="text" id="userInput" placeholder="Waiting for command, Sir..." onkeypress="if(event.key=='Enter') ask()">
        <button onclick="ask()">SEND</button>
    </div>

    <script>
        async function ask() {
            let input = document.getElementById('userInput').value;
            if(!input) return;
            let chat = document.getElementById('chat');
            
            chat.innerHTML += `<div class="msg user"><b>Sir:</b> ${input}</div>`;
            document.getElementById('userInput').value = '';
            chat.scrollTop = chat.scrollHeight;

            try {
                let response = await fetch('/chat?msg=' + encodeURIComponent(input));
                let data = await response.json();
                chat.innerHTML += `<div class="msg jarvis"><b>Jarvis:</b> ${data.reply}</div>`;
            } catch(e) {
                chat.innerHTML += `<div class="msg jarvis">Sir, link timeout. Please retry.</div>`;
            }
            chat.scrollTop = chat.scrollHeight;
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
            model='DeepSeek-V3.1',
            messages=[
                {"role": "system", "content": "You are Jarvis, the witty and loyal AI of Arslan Sir. Keep it classy."},
                {"role": "user", "content": user_msg}
            ]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Sir, neural link error: {str(e)}"})

if __name__ == '__main__':
    # Replit requires port 8080 and host 0.0.0.0
    app.run(host='0.0.0.0', port=8080)