🧙‍♂️ Wiki-Gnome
Turn Slack chaos into a beautiful, searchable Knowledge Base instantly.

🚨 The Problem
Remote teams drown in noise. Important decisions, bug fixes, and feature ideas happen in Slack threads, but they get buried under hundreds of messages.

Lost Context: "Why did we make that decision?"

Repetition: "How do I fix this bug again?"

Accessibility: "I don't have time to read 50 messages."

✨ The Solution
Wiki-Gnome is an invisible agent that lives in your Slack. It watches for Emoji Triggers. When you react to a thread, Wiki-Gnome uses Gemma 2 (via Groq) to analyze the conversation and transform it into a permanent asset on a Live Dashboard.

It doesn't just summarize. It categorizes, visualizes, and even speaks.

🎮 Features & Triggers
Wiki-Gnome is a "Swiss Army Knife" for productivity. Just click an emoji:

Emoji	Mode	What it does
📝 Memo	Documentation	Converts technical chat into a formatted Markdown doc.
🐛 Bug	Bug Report	Extracts the Issue, Reproduction Steps, and the Fix.
💡 Bulb	Feature Idea	Extracts the Pitch and User Benefits.
✅ Check	Task List	Creates an actionable checklist of WHO needs to do WHAT.
🎧 Headphones	Audio Catch-up	(Accessibility) Generates a 30s MP3 news summary of the thread.
🔥 Fire	Roast Mode	Gordon Ramsay style code review (Just for fun!).
🖥️ The Live Dashboard
Wiki-Gnome comes with a built-in Real-Time Dashboard styled with Google's design system.

Auto-Refreshes every 5 seconds.

Visual Cards for every document.

Zero-Database: Uses a flat-file system for maximum simplicity and portability.

🛠️ Architecture
Code snippet
graph LR
    A[Slack User] -- Reacts 📝 --> B[Wiki-Gnome Bot]
    B -- Transcript --> C[Groq API (Gemma 2)]
    C -- JSON Summary --> B
    B -- Save File --> D[Local KB Folder]
    B -- Generate Audio --> E[gTTS Engine]
    D --> F[Live Dashboard (FastAPI/Jinja2)]
🚀 Quick Start
1. Clone & Install

Bash
git clone https://github.com/yourusername/wiki-gnome.git
cd wiki-gnome
pip install -r requirements.txt
2. Configure Keys

Create a .env file:

Ini, TOML
GROQ_API_KEY=gsk_...
SLACK_BOT_TOKEN=xoxb-...
3. Run the Engine

Terminal 1 (The Brain):

Bash
uvicorn main:app --reload --port 8000
Terminal 2 (The Tunnel):

Bash
python tunnel.py
4. Experience It

Slack: Invite @Wiki-Gnome to a channel.

Dashboard: Open http://localhost:8000/dashboard.

🧠 Powered By
FastAPI: For the high-speed backend.

Groq: For near-instant AI inference.

Gemma 2 (9b): The open model powering the intelligence.

gTTS: For on-device text-to-speech generation.
