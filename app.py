from flask import Flask, render_template_string, request, jsonify
import os
import openai
import json

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')

# Load persona info
PERSONA_PATH = "persona.json"
with open(PERSONA_PATH, "r", encoding="utf-8") as f:
    PERSONA = json.load(f)

# OpenAI setup
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("WARNING: OPENAI_API_KEY not set! AI responses will fail.")

# In-memory state
is_dead = False
history = []

# HTML template
HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>DeadBot Demo — {{ label }} (SIMULATION)</title>
<style>
body{font-family:system-ui,Segoe UI,Arial;max-width:900px;margin:22px auto;padding:12px}
#log{border:1px solid #ddd;padding:12px;height:360px;overflow:auto;background:#fff}
.you{color:navy}
.bot{color:darkred}
.system{color:gray;font-size:0.9em}
.badge{display:inline-block;padding:6px 8px;background:#fff2f2;border:1px solid #ffcccc;color:#a00;border-radius:6px;margin-left:8px}
button{margin-left:6px}
</style>
</head>
<body>
<h1>DeadBot Demo — {{ label }} (SIMULATION)</h1>
<div>
  <strong id="personaLabel">{{ label }}</strong>
  <span class="badge">[SIMULATION — PUBLIC FIGURE]</span>
  <p id="personaProfile" class="system">{{ profile }}</p>
</div>
<div id="log"></div>
<div class="controls" style="margin-top:12px">
<input id="msg" placeholder="Type your message..." style="width:70%">
<button id="send">Send</button>
<button id="die">Simulate Dead</button>
<button id="revive">Revive</button>
</div>
<script>
const log = document.getElementById('log');
const msg = document.getElementById('msg');
const sendBtn = document.getElementById('send');
const dieBtn = document.getElementById('die');
const reviveBtn = document.getElementById('revive');
function append(who, text, cls){
  const d = document.createElement('div');
  d.innerHTML = `<b class="${cls}">${who}:</b> ${text}`;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}
async function postChat(message){
  append('You', message, 'you');
  const payload = { message };
  try {
    const r = await fetch('/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const j = await r.json();
    if(r.ok){
      append('DeadBot', j.bot, 'bot');
    } else {
      append('SYSTEM', 'ERROR: ' + (j.error || 'unknown'), 'system');
    }
  } catch(e){
    append('SYSTEM', 'Network error: ' + e, 'system');
  }
}
sendBtn.onclick = () => { const t = msg.value.trim(); if(!t) return; postChat(t); msg.value=''; };
msg.addEventListener('keydown', (e) => { if(e.key === 'Enter') sendBtn.click(); });
dieBtn.onclick = async () => {
  await fetch('/toggle_dead', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({dead:true})});
  append('SYSTEM','DeadBot state: DEAD','system');
};
reviveBtn.onclick = async () => {
  await fetch('/toggle_dead', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({dead:false})});
  append('SYSTEM','DeadBot state: ALIVE','system');
};
append('SYSTEM','This demo simulates Liam Payne. All replies are fictional and marked [SIMULATION].','system');
</script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(
        HTML,
        label=PERSONA.get("name", "DeadBot"),
        profile=PERSONA.get("description", "")
    )

@app.route('/chat', methods=['POST'])
def chat():
    global is_dead, history
    data = request.get_json() or {}
    message = (data.get('message') or "").strip()
    if not message:
        return jsonify({"error":"No message provided."}), 400
    if is_dead:
        return jsonify({"bot":"... (no response — simulated dead state)"})

    prompt = f"""
You are simulating Liam Payne, the British singer and former member of One Direction.
Speak casually and friendly as Liam would. Keep responses short (1-2 sentences).
User said: {message}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI API error:", e)
        reply = "[SIMULATION] Sorry, I am unable to respond right now."

    history.append({"user": message, "bot": reply})
    history = history[-40:]
    return jsonify({"bot": reply})

@app.route('/toggle_dead', methods=['POST'])
def toggle_dead():
    global is_dead
    data = request.get_json() or {}
    is_dead = bool(data.get('dead', False))
    return jsonify({"dead": is_dead})

@app.route('/persona', methods=['GET'])
def persona():
    return jsonify(PERSONA)

# Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
