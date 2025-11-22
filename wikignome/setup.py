import os

# 1. Create Folders
folders = ["kb/docs", "kb/bugs", "kb/ideas", "kb/tasks", "kb/audio", "templates"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Created folder: {folder}")

# 2. Create Requirements.txt
reqs = "fastapi\nuvicorn\nslack-sdk\ngroq\npython-dotenv\nmarkdown\njinja2\ngTTS"
with open("requirements.txt", "w") as f:
    f.write(reqs)
print("✅ Created requirements.txt")

# 3. Create .env Template
env_text = "GROQ_API_KEY=paste_key_here\nSLACK_BOT_TOKEN=paste_token_here"
with open(".env", "w") as f:
    f.write(env_text)
print("✅ Created .env file")

# 4. Create the "Ashini" Google Dashboard
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5">
    <title>Wiki-Gnome HQ</title>
    <style>
        :root { --blue: #4285F4; --red: #EA4335; --yellow: #FBBC05; --green: #34A853; --bg: #ffffff; }
        body { font-family: 'Product Sans', Arial, sans-serif; background: var(--bg); padding: 40px; color: #202124; }
        header { border-bottom: 1px solid #dadce0; padding-bottom: 20px; margin-bottom: 40px; }
        h1 { font-size: 2.5rem; margin: 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; }
        .card { background: white; border: 1px solid #dadce0; border-radius: 8px; padding: 20px; text-decoration: none; color: inherit; position: relative; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.12); }
        .card:hover { box-shadow: 0 4px 12px rgba(60,64,67,0.15); transform: translateY(-2px); transition: 0.2s; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 6px; }
        .card.docs::before { background: var(--blue); }
        .card.bugs::before { background: var(--red); }
        .card.ideas::before { background: var(--yellow); }
        .card.tasks::before { background: var(--green); }
        .card.audio::before { background: #9334E6; }
        .type { font-size: 0.75rem; font-weight: bold; text-transform: uppercase; color: #5f6368; display: block; margin-bottom: 8px; }
        .title { font-size: 1.1rem; font-weight: bold; display: block; margin-bottom: 8px; }
        .meta { font-size: 0.85rem; color: #5f6368; }
    </style>
</head>
<body>
    <header>
        <h1>Wiki-Gnome <span style="color:#4285F4">H</span><span style="color:#EA4335">Q</span></h1>
        <div style="color: #5f6368; margin-top: 10px; font-size: 1.2rem;">Hey Ashini! 👋 Here are your latest updates.</div>
    </header>
    <div class="grid">
        {% for file in files %}
        <a href="#" class="card {{ file.type }}">
            <span class="type">{{ file.type }}</span>
            <span class="title">{{ file.name }}</span>
            <div class="meta">{{ file.icon }} {{ file.date }}</div>
        </a>
        {% endfor %}
    </div>
</body>
</html>
"""
with open("templates/dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("✅ Created Dashboard HTML")
print("🚀 SETUP COMPLETE!")