# 🐍 PyTutor AI — Ms. Aanya

> An AI-powered Python tutor for school students (ages 10–16), built with Flask + Groq (free LLaMA 3.3 70B). Features a talking animated avatar, live captions, a code editor, whiteboard, quizzes, and a progress dashboard — all in just **two files**.

---

## ✨ Features

- 🧑‍🏫 **Animated AI Tutor** — Ms. Aanya talks, blinks, and lip-syncs in real time
- 💬 **Chat Mode** — Ask any Python question, get warm encouraging answers
- 🖊️ **Whiteboard Mode** — Visual topic explanations with diagrams
- 💻 **Code Editor** — Syntax-highlighted lessons with live output
- 🧪 **Online Compiler** — Run Python code right in the browser
- 📝 **Practice Questions** — Graded coding challenges with hints
- 🧠 **Quick Quizzes** — Per-topic MCQ quizzes to test understanding
- 📊 **Dashboard** — Track visited topics, quiz scores, and strengths/weaknesses
- 🎙️ **Voice Input** — Speak your questions using the mic button
- 🌙 / 🌞 **Dark & Light Mode** — Warm amber light theme + cool dark theme
- 📚 **Full Syllabus** — 20+ topics from Hello World to File I/O and Modules

---

## 🗂️ Project Structure

```
pytutor-ai/
├── app.py          # Flask backend — AI chat, code runner, API routes
├── tutor.html      # Full frontend UI — served directly by Flask
└── requirements.txt
```

That's it. No build tools, no npm, no separate frontend server.

---

## ⚡ Quick Start

### 1. Get a free Groq API key
Go to [console.groq.com](https://console.groq.com) → API Keys → Create API Key.
Takes 30 seconds, no credit card needed.

### 2. Install dependencies

```bash
pip install flask groq
```

### 3. Add your API key

Open `app.py` and paste your key:

```python
GROQ_API_KEY = "gsk_your_key_here"
```

Or set it as an environment variable (recommended):

```bash
# Mac/Linux
export GROQ_API_KEY=gsk_your_key_here

# Windows
set GROQ_API_KEY=gsk_your_key_here
```

### 4. Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🚀 Deploy to Production

### Railway (Recommended — free, ~5 min)

1. Push your files to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variable: `GROQ_API_KEY = gsk_...`
4. Railway auto-detects Flask and gives you a live URL

### Render (Free tier)

1. Push to GitHub with `requirements.txt`
2. Go to [render.com](https://render.com) → New Web Service
3. Set start command: `python app.py`
4. Add `GROQ_API_KEY` in Environment Variables

> ⚠️ **Before pushing to GitHub**, remove the hardcoded API key from `app.py` and use environment variables instead so your key stays private.

---

## 🧰 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the tutor UI |
| `POST` | `/api/chat` | Main chat — student message → AI reply |
| `POST` | `/api/explain` | Re-explain current topic fresh |
| `POST` | `/api/run` | Execute Python code server-side |
| `GET` | `/api/status` | Check if API key is configured |

### Example chat request

```json
POST /api/chat
{
  "message": "What is a variable?",
  "topic": "variables",
  "history": []
}
```

---

## 🤖 AI Model

Powered by **Groq** running **LLaMA 3.3 70B** (`llama-3.3-70b-versatile`).

- Completely free on Groq's generous free tier
- Very fast inference (Groq's custom hardware)
- Ms. Aanya's personality is defined in the system prompt in `app.py` — feel free to customize it

---

## 📚 Syllabus Covered

| Chapter | Topics |
|---------|--------|
| Python Basics | Intro, Installation, Hello World, Comments |
| Data & Variables | Data Types, Variables, User Input, Operators |
| Control Flow | If/Else, For Loops, While Loops, Break & Continue |
| Functions | Defining Functions, Parameters & Return, Variable Scope |
| Data Structures | Lists, Tuples, Dictionaries, Sets |
| Strings | String Methods & Formatting |
| Advanced | File Handling, Error Handling, Modules & Imports |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI | Groq API (LLaMA 3.3 70B) |
| Frontend | Vanilla HTML/CSS/JS (no frameworks) |
| TTS | Web Speech API (browser built-in) |
| STT | Web Speech Recognition API |
| Code Runner | Piston API + Flask fallback |

---

## 🙋 Customisation Tips

- **Change the tutor's personality** — edit `SYSTEM_PROMPT` in `app.py`
- **Change the AI model** — update `GROQ_MODEL` (see [Groq docs](https://console.groq.com/docs/models) for available models)
- **Add topics to the syllabus** — edit the `syllabus` array in `tutor.html`
- **Add practice questions** — edit the `practiceQs` array in `tutor.html`
- **Change avatar appearance** — edit the inline SVG inside `.avatar-ring` in `tutor.html`

---

*Built with ❤️ for students learning Python*
