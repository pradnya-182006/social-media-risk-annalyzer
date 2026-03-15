import time
import json
import os
from plyer import notification

CONFIG_FILE = 'screen_config.json'

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"limit": 4.0, "status": "active", "start_time": time.time()}

def send_alert(message):
    try:
        notification.notify(
            title='🚀 MindBalance: Screen Time Alert',
            message=message,
            app_name='MindBalance AI',
            timeout=10
        )
    except:
        print(f"Alert: {message}")

def monitor():
    print("MindBalance Monitor Started in Background...")
    last_alert_time = 0
    
    while True:
        config = get_config()
        if config["status"] == "active":
            # Simulate tracking: In a real app, this would poll OS usage APIs.
            # Here we track the 'session' duration since the background agent started
            elapsed_hours = (time.time() - config["start_time"]) / 3600
            limit = config["limit"]
            
            if elapsed_hours > limit:
                # Alert every 15 minutes if over limit
                if time.time() - last_alert_time > 900: 
                    send_alert(f"⚠️ DANGER: You are {elapsed_hours:.1f}h over your limit! Close social media now.")
                    last_alert_time = time.time()
        
        time.sleep(60) # Poll every minute

if __name__ == "__main__":
    monitor()
