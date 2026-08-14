import os
import requests

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_alert():
    message = {
        "text": "⚠️ *Animal Detected on Railway Track!* \nPlease take immediate action."
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print("✅ Slack alert sent successfully.")
        else:
            print(f"❌ Slack alert failed: {response.status_code} {response.text}")
    except Exception as e:
        print("❌ Error sending Slack alert:", e)
