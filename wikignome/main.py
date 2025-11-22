import os
import re
import json
from datetime import datetime
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from slack_sdk import WebClient
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Config
BASE_FOLDER = "kb"
EMOJI_MODES = {
    "memo": { "action": "file", "type": "docs", "icon": "📝", "prompt": "Summarize into documentation." },
    "bug": { "action": "file", "type": "bugs", "icon": "🐛", "prompt": "Extract Issue, Steps, Fix." },
    "bulb": { "action": "file", "type": "ideas", "icon": "💡", "prompt": "Extract Pitch and Benefits." },
    "white_check_mark": { "action": "file", "type": "tasks", "icon": "✅", "prompt": "Create Task Checklist." },
    "headphones": { "action": "audio", "type": "audio", "icon": "🎧", "prompt": "Write a news script." },
    "fire": { "action": "roast", "type": "fun", "icon": "🔥", "prompt": "Roast this code." }
}

slack = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def sanitize(title): return re.sub(r'[^a-z0-9]', '_', title.lower()).strip('_')

@app.get("/dashboard")
async def dashboard(request: Request):
    files_list = []
    for type_name in ["docs", "bugs", "ideas", "tasks", "audio"]:
        path = os.path.join(BASE_FOLDER, type_name)
        if os.path.exists(path):
            for f in os.listdir(path):
                icon = next((v['icon'] for k,v in EMOJI_MODES.items() if v['type'] == type_name), "📄")
                date = datetime.fromtimestamp(os.path.getmtime(os.path.join(path, f))).strftime('%H:%M')
                files_list.append({"name": f, "type": type_name, "date": date, "icon": icon})
    files_list.sort(key=lambda x: x['date'], reverse=True)
    return templates.TemplateResponse("dashboard.html", {"request": request, "files": files_list})

# REPLACE THE OLD process_event WITH THIS LOUD VERSION
async def process_event(channel, ts, reaction):
    print(f"👀 I SAW A REACTION: {reaction}") # <--- Debug Print 1
    
    if reaction not in EMOJI_MODES: 
        print(f"❌ IGNORING: {reaction} is not in my list.")
        return
    
    mode = EMOJI_MODES[reaction]
    print(f"✅ MODE ACTIVATED: {mode['type']}") # <--- Debug Print 2
    
    try:
        # Get Chat History
        history = slack.conversations_replies(channel=channel, ts=ts)
        transcript = ""
        authors = []
        for m in history['messages']:
            if "bot_id" in m: continue
            name = slack.users_info(user=m['user'])['user']['real_name']
            transcript += f"[{name}]: {m.get('text','')}\n"
            authors.append(name)
            
        if not transcript: 
            print("❌ ERROR: Transcript was empty!")
            return

        print("🧠 SENDING TO GROQ AI...") # <--- Debug Print 3
        sys_prompt = f"{mode['prompt']} Output JSON: {{\"title\": \"Short Title\", \"summary\": \"Content\"}}"
        completion = groq.chat.completions.create(model="gemma2-9b-it", messages=[{"role":"system","content":sys_prompt},{"role":"user","content":transcript}], response_format={"type":"json_object"})
        res = json.loads(completion.choices[0].message.content)
        print(f"🤖 AI RESPONDED: {res['title']}") # <--- Debug Print 4

        if mode['action'] == "file":
            filename = f"{sanitize(res['title'])}.md"
            path = os.path.join(BASE_FOLDER, mode['type'], filename)
            with open(path, "w") as f: f.write(f"# {res['title']}\n**Authors:** {', '.join(set(authors))}\n\n{res['summary']}")
            slack.reactions_add(channel=channel, name="floppy_disk", timestamp=ts)
            slack.chat_postMessage(channel=channel, thread_ts=ts, text=f"Saved to Dashboard!")
            print(f"💾 FILE SAVED TO: {path}") # <--- Debug Print 5

        elif mode['action'] == "audio":
            filename = f"{sanitize(res['title'])}.mp3"
            path = os.path.join(BASE_FOLDER, "audio", filename)
            gTTS(text=res['summary'], lang='en').save(path)
            slack.files_upload_v2(channel=channel, file=path, title=res['title'], initial_comment="🎧 Audio Summary")

        elif mode['action'] == "roast":
            slack.chat_postMessage(channel=channel, thread_ts=ts, text=f"🔥 {res['summary']}")
            
    except Exception as e: 
        print(f"💀 CRITICAL ERROR: {e}") # <--- This will tell us exactly what is wrong

@app.post("/slack/events")
async def slack_endpoint(request: Request, bt: BackgroundTasks):
    data = await request.json()
    if "challenge" in data: return {"challenge": data["challenge"]}
    if data.get("event", {}).get("type") == "reaction_added":
        ev = data["event"]
        bt.add_task(process_event, ev["item"]["channel"], ev["item"]["ts"], ev["reaction"])
    return {"status": "ok"}

    # REPLACE THE BOTTOM FUNCTION WITH THIS X-RAY VERSION
@app.post("/slack/events")
async def slack_endpoint(request: Request, bt: BackgroundTasks):
    data = await request.json()
    
    # 1. PRINT THE RAW DATA (This is the X-Ray)
    print("------------------------------------------------")
    print(f"📨 INCOMING DATA: {data}") 
    print("------------------------------------------------")

    # Handle the Challenge (Connects Slack)
    if "challenge" in data: 
        print("✅ responding to challenge")
        return {"challenge": data["challenge"]}
    
    event = data.get("event", {})
    event_type = event.get("type")
    
    print(f"🧐 EVENT TYPE DETECTED: {event_type}")

    # Check if it is a reaction
    if event_type == "reaction_added":
        print("🚀 IT IS A REACTION! STARTING PROCESS...")
        bt.add_task(process_event, event["item"]["channel"], event["item"]["ts"], event["reaction"])
    else:
        print("💤 Ignoring this event (Not a reaction)")

    return {"status": "ok"}