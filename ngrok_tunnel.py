from pyngrok import ngrok
import time

# Set the authtoken
ngrok.set_auth_token("3BFz0AnRGAqPNzSHevZz23tyomX_71ptJEfgqyrHCW8syJU4w")

# Start a tunnel on port 8501
try:
    public_url = ngrok.connect(8501)
    print(f"NGROK_URL: {public_url}")
    # Write to file for Antigravity to read
    with open("ngrok_public_url.txt", "w") as f:
        f.write(str(public_url))
    
    # Keep the script running to maintain the tunnel
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping tunnel...")
except Exception as e:
    print(f"Error: {e}")
