from pyngrok import ngrok
import time

# Open a tunnel on port 8000
print("🚀 Opening Tunnel...")
try:
    public_url = ngrok.connect(8000).public_url
    print("--------------------------------------------------")
    print("🎉 SUCCESS! YOUR URL IS:")
    print(public_url)
    print("--------------------------------------------------")
    print("1. Copy this URL.")
    print("2. Go to Slack -> Event Subscriptions.")
    print("3. Paste it and add '/slack/events'.")
    
    # Keep running
    while True:
        time.sleep(1)
except Exception as e:
    print(f"Error: {e}")
    print("You might need to add your token. Run: ngrok config add-authtoken YOUR_TOKEN")