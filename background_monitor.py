import time
import json
import os
from plyer import notification

CONFIG_FILE = 'screen_config.json'

from datetime import datetime

def get_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"limit": 4.0, "status": "active", "date": datetime.now().strftime("%Y-%m-%d"), "elapsed_time": 0.0, "last_update_time": time.time()}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

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
        current_time = time.time()
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if config.get("date") != current_date:
            config["date"] = current_date
            config["elapsed_time"] = 0.0
            config["last_update_time"] = current_time
            save_config(config)
            
        if config.get("status") == "active":
            last_update = config.get("last_update_time", current_time)
            delta = current_time - last_update
            
            # If delta is between 0 and 5 minutes, add to elapsed time.
            # A larger delta means the PC was asleep/off.
            if 0 < delta < 300:
                config["elapsed_time"] = config.get("elapsed_time", 0.0) + delta
                
            config["last_update_time"] = current_time
            save_config(config)
            
            elapsed_minutes = config.get("elapsed_time", 0.0) / 60.0
            limit_m = float(config.get("limit", 4.0)) * 60.0
            
            if elapsed_minutes > limit_m:
                # Alert every 15 minutes if over limit
                if current_time - last_alert_time > 900: 
                    send_alert(f"⚠️ DANGER: You are {elapsed_minutes:.1f}m over your limit! Close social media now.")
                    last_alert_time = current_time
        
        time.sleep(60) # Poll every minute

if __name__ == "__main__":
    monitor()
