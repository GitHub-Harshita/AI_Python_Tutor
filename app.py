"""
Ms. Aanya — AI Python Tutor  (SINGLE FILE — just run this!)
=============================================================
SETUP:
  1. pip install flask groq
  2. Paste your FREE Groq key below  (get it at https://console.groq.com)
  3. python app.py
  4. Open http://localhost:5000

Everything — the AI backend AND the full tutor UI — is in this one file.
No other files needed!
"""

from flask import Flask, request, jsonify
import re, os

app = Flask(__name__)

# ══════════════════════════════════════════════════════════
#  ▶  PASTE YOUR FREE GROQ API KEY HERE  ◀
#  Get it free (no credit card) at: https://console.groq.com
#  Click "API Keys" → "Create API Key" → Copy and paste below
GROQ_API_KEY = "Enter your API Key"
# ══════════════════════════════════════════════════════════
# Or set as environment variable:
#   Windows:   set GROQ_API_KEY=gsk_...
#   Mac/Linux: export GROQ_API_KEY=gsk_...
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", GROQ_API_KEY)

# Groq model — llama-3.3-70b is free, smart, and fast
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are Ms. Aanya, a warm, enthusiastic Python teacher for school students (ages 10-16) in India.

Your personality:
- Encouraging, patient, friendly — never make the student feel stupid
- Use simple everyday analogies (cricket, food, Bollywood, daily life in India) when explaining
- Celebrate wins with phrases like: Excellent! You are getting it! Well done! Shabash!
- Avoid jargon — always explain technical terms in the simplest way
- Keep responses to 3-5 sentences unless the student asks for more detail

Your teaching style:
- Always relate the concept to real life FIRST, then explain the Python
- Give a simple explanation then one short example
- If a student seems confused, try a completely different analogy
- Never dump raw code without walking through what each part does
- If asked to explain again, give a FRESH explanation with a NEW analogy

STRICT formatting rules — follow these exactly:
- Write in plain natural sentences ONLY
- Absolutely NO markdown — no asterisks, no bold, no bullet points, no hashtags, no backticks
- No numbered lists
- Conversational and warm, like a real teacher talking face to face with a student
- Always end with either an encouraging phrase or a question to keep the student engaged"""


def clean_text(text: str) -> str:
    """Strip any markdown that sneaks through."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`{1,3}([^`]*)`{1,3}', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-•*\d+\.]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def groq_chat(message: str, topic: str = "", history: list = None) -> str:
    """Send a message to Groq and get Ms. Aanya's reply."""
    key = GROQ_API_KEY.strip()

    if not key or key == "YOUR_GROQ_API_KEY_HERE":
        return ("Ms. Aanya is not connected yet! Open app.py and paste your free Groq API key "
                "where it says GROQ_API_KEY. Get a free key in 30 seconds at console.groq.com "
                "— no credit card needed.")

    try:
        from groq import Groq
        client = Groq(api_key=key)

        # Build messages list for the API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history (last 6 messages for context)
        for msg in (history or [])[-6:]:
            role = msg.get("role", "user")
            content = msg.get("content", "").strip()
            if content and role in ("user", "assistant"):
                messages.append({"role": role, "content": content})

        # Add topic context to the current message
        full_message = message
        if topic:
            full_message = f"[The student is currently studying: {topic}]\n\nStudent: {message}"

        messages.append({"role": "user", "content": full_message})

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )

        reply = response.choices[0].message.content.strip()
        return clean_text(reply)

    except ImportError:
        return "Please run: pip install groq — then restart the server."
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower() or "authentication" in err.lower():
            return ("Your Groq API key seems incorrect. Open app.py, fix the GROQ_API_KEY value, "
                    "and restart the server.")
        if "429" in err or "rate_limit" in err.lower():
            return ("I am thinking a little too fast! Please wait just a few seconds and try again. "
                    "Groq free tier is very generous so this will clear up quickly.")
        if "503" in err or "unavailable" in err.lower():
            return "Groq servers are busy right now. Please try again in a moment!"
        # Log the actual error to console for debugging
        print(f"[Groq Error] {err}")
        return "I had a small hiccup. Please try again!"


# ─── Flask Routes ──────────────────────────────────────────────────────────────

# ─── HTML is embedded here — no separate tutor.html file needed ───────────────
import os as _os

_THIS_DIR = _os.path.dirname(_os.path.abspath(__file__))
_HTML_PATH = _os.path.join(_THIS_DIR, 'tutor.html')

def _load_html():
    with open(_HTML_PATH, 'r', encoding='utf-8') as _f:
        return _f.read()

@app.route("/")
def index():
    """Serve the tutor UI from tutor.html."""
    return _load_html()


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Main chat endpoint — student message → Groq → reply."""
    data    = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    topic   = data.get("topic", "")
    history = data.get("history", [])

    if not message:
        return jsonify({"reply": "I did not catch that — could you ask again?"})

    reply = groq_chat(message, topic, history)
    return jsonify({"reply": reply})


@app.route("/api/explain", methods=["POST"])
def api_explain():
    """Re-explain the current topic in a fresh way."""
    data  = request.get_json(silent=True) or {}
    topic = data.get("topic", "Python")
    style = data.get("style", "normal")

    style_map = {
        "simple":   "Use the simplest possible words and a fun everyday Indian analogy. 3-4 sentences only.",
        "normal":   "Give a clear engaging explanation with a good analogy. 4-6 sentences.",
        "detailed": "Explain thoroughly: what it is, why it matters, and walk through a real example. 6-8 sentences.",
    }
    prompt = (f"Please explain '{topic}' in Python to a school student in a completely fresh way. "
              f"{style_map.get(style, style_map['normal'])} Plain sentences only, absolutely no markdown.")

    reply = groq_chat(prompt)
    return jsonify({"explanation": reply if reply else None})


@app.route("/api/status")
def api_status():
    """Frontend can check if the key is configured."""
    key = GROQ_API_KEY.strip()
    configured = bool(key and key != "YOUR_GROQ_API_KEY_HERE")
    return jsonify({"configured": configured, "provider": "Groq"})



@app.route("/api/run", methods=["POST"])
def api_run():
    """Execute Python code server-side as fallback compiler."""
    import subprocess, sys
    data = request.get_json(silent=True) or {}
    code  = data.get("code", "")
    stdin = data.get("stdin", "")
    if not code.strip():
        return jsonify({"output": "", "error": "No code provided."})
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            input=stdin, capture_output=True, text=True, timeout=10
        )
        return jsonify({"output": result.stdout, "error": result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "", "error": "Code timed out (10s limit)."})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    key    = GROQ_API_KEY.strip()
    key_ok = bool(key and key != "YOUR_GROQ_API_KEY_HERE")

    print("\n" + "="*55)
    print("  Ms. Aanya — AI Python Tutor  (single file, powered by Groq)")
    print("="*55)
    print(f"  URL   : http://localhost:{port}")
    if key_ok:
        print(f"  AI    : Groq connected  [{GROQ_MODEL}]")
        print(f"  Key   : {key[:10]}...")
    else:
        print("  AI    :  No API key set!")
        print("  Fix   : Open app.py → set GROQ_API_KEY")
        print("  Key   : https://console.groq.com  (free, 30 sec)")
    print("="*55 + "\n")

    app.run(debug=True, host="0.0.0.0", port=port)
